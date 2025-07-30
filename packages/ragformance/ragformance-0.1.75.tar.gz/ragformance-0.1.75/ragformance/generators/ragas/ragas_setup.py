import importlib
import subprocess
import sys
from typing import Tuple, Type
import inspect
import warnings
import json
import os

from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas.llms import LangchainLLMWrapper
from ragas.testset import TestsetGenerator

from ragas.testset.synthesizers.multi_hop import (
    MultiHopAbstractQuerySynthesizer,
    MultiHopSpecificQuerySynthesizer,
)
from ragas.testset.synthesizers.single_hop.specific import (
    SingleHopSpecificQuerySynthesizer,
)
from ragas.testset.synthesizers import QueryDistribution

# Pipeline id from the config .json
PIPELINE_ID = "ragas"

# Provider: (pip_package, chat_module, chat_class, embeddings_module, embeddings_class)
PROVIDER_REGISTRY = {
    "openai": (
        "langchain-openai",
        "langchain_openai.chat_models",
        "ChatOpenAI",
        "langchain_openai.embeddings",
        "OpenAIEmbeddings",
    ),
    "anthropic": (
        "langchain-anthropic",
        "langchain_anthropic.chat_models",
        "ChatAnthropic",
        "langchain_anthropic.embeddings",
        "AnthropicEmbeddings",
    ),
    "mistralai": (
        "langchain-mistralai",
        "langchain_mistralai.chat_models",
        "ChatMistralAI",
        "langchain_mistralai.embeddings",
        "MistralAIEmbeddings",
    ),
    "groq": (
        "langchain-groq",
        "langchain_groq.chat_models",
        "ChatGroq",
        "langchain_groq.embeddings",
        "GroqEmbeddings",
    ),
    "ollama": (
        "langchain-ollama",
        "langchain_ollama.chat_models",
        "ChatOllama",
        "langchain_ollama.embeddings",
        "OllamaEmbeddings",
    ),
    "huggingface": (
        "langchain-huggingface",
        "langchain_huggingface.chat_models",
        "ChatHuggingFace",
        "langchain_huggingface.embeddings",
        "HuggingFaceEmbeddings",
    ),
    "fireworks": (
        "langchain-fireworks",
        "langchain_fireworks.chat_models",
        "ChatFireworks",
        "langchain_fireworks.embeddings",
        "FireworksEmbeddings",
    ),
    "deepseek": (
        "langchain-deepseek",
        "langchain_deepseek.chat_models",
        "ChatDeepSeek",
        "langchain_deepseek.embeddings",
        "DeepSeekEmbeddings",
    ),
    "perplexity": (
        "langchain-perplexity",
        "langchain_perplexity.chat_models",
        "ChatPerplexity",
        "langchain_perplexity.embeddings",
        "PerplexityEmbeddings",
    ),
    "xai": (
        "langchain-xai",
        "langchain_xai.chat_models",
        "ChatXAI",
        "langchain_xai.embeddings",
        "XAIEmbeddings",
    ),
    "cohere": (
        "langchain-cohere",
        "langchain_cohere.chat_models",
        "ChatCohere",
        "langchain_cohere.embeddings",
        "CohereEmbeddings",
    ),
    "together": (
        "langchain-together",
        "langchain_together.chat_models",
        "ChatTogether",
        "langchain_together.embeddings",
        "TogetherEmbeddings",
    ),
    # Extend as needed
}

# Map the JSON question_type → your classes
QUESTION_SYNTHESIZERS = {
    "singlehop-specific": SingleHopSpecificQuerySynthesizer,
    "multihop-specific": MultiHopSpecificQuerySynthesizer,
    "multihop-abstract": MultiHopAbstractQuerySynthesizer,
}


def _validate_langchain_args(provider, class_instance, class_type, **kwargs):
    # The additional arguments must comply with the obtained llmchat class from langchain

    if class_type == "llm":
        JSON_TARGET_FIELD = "llms"
    elif class_type == "embedding":
        JSON_TARGET_FIELD = "embeddings"

    # Get the signature of the method
    sig = inspect.signature(class_instance)

    # Get arguments from the method TestsetGenerator.generate
    valid_arg_names = [
        name
        for name in sig.parameters
        if name != "self"  # usually omit 'self'
    ]

    valid_arg_aliases = [
        field.alias
        for name, field in class_instance.__fields__.items()
        if field.alias and field.alias != name
    ]

    valid_arg_names += valid_arg_aliases

    # Find any unexpected arguments on **kwargs[langchain_provider]

    unexpected_langchain_args = [
        key for key in kwargs["langchain_provider"] if key not in valid_arg_names
    ]

    if unexpected_langchain_args:
        raise ValueError(
            f"\n RAGAS-ERROR: {class_instance} with unexpected argument(s) : {', '.join(unexpected_langchain_args)}.\n"
            f"Valid arguments for {class_instance} are: {', '.join(sorted(valid_arg_names))}\n\n"
            f"Please, correct the config.json file: \n"
            f"\t - Locate the {JSON_TARGET_FIELD} with provider '{provider}'\n"
            f"\t - In 'params':{{...'langchain_provider': ...\}} \n"
            f"\t - Fields must comply with the valid argument list above\n"
        )

    # Find any unexpected arguments from the rest of common **kwargs
    common_kwargs = {}

    for key, val in kwargs.items():
        if key in ["langchain_provider", "langchain_rate_limiter"]:
            # skip this entire nested dict
            continue
        if isinstance(val, dict):
            warnings.warn(
                f"\n RAGAS-WARNING: Configuration parameters (.json) {{...'params': ... '{key}':...}} for '{provider}' {JSON_TARGET_FIELD} not used/ignored."
            )
            continue
        else:
            common_kwargs[key] = val

    unexpected_common_kargs = [
        key for key in common_kwargs if key not in valid_arg_names
    ]

    if unexpected_common_kargs:
        warnings.warn(
            f"\n RAGAS-WARNING: {class_instance} will IGNORE argument(s) : {', '.join(unexpected_common_kargs)}.\n"
            f"Valid arguments for {class_instance} are: {', '.join(sorted(valid_arg_names))}\n\n"
            f"Please, ensure in your config.json file: \n"
            f"\t - Locate the {JSON_TARGET_FIELD} with provider '{provider}'\n"
            f"\t - Create in 'params' a dict called: 'langchain_provider'\n"
            f"\t - Within 'langchain_provider', add the equivalent arguments of interest from the compatible list above."
        )

    # Return only valid parameters
    return {
        **{
            key: value
            for key, value in common_kwargs.items()
            if key in valid_arg_names and value is not None
        },
        **{
            key: value
            for key, value in kwargs["langchain_provider"].items()
            if key in valid_arg_names and value is not None
        },
    }


def get_llmchat_instance(provider: str, **kwargs) -> Tuple[Type, Type]:
    """Return both chat and embedding classes for a given provider."""
    if provider not in PROVIDER_REGISTRY:
        raise ValueError(f"Unknown provider: {provider}")

    (
        pip_package,
        chat_module_path,
        chat_class_name,
        embeddings_module_path,
        embeddings_class_name,
    ) = PROVIDER_REGISTRY[provider]

    try:
        chat_module = importlib.import_module(chat_module_path)
    except ImportError:
        print(f"Installing missing package: {pip_package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_package])
        chat_module = importlib.import_module(chat_module_path)

    chat_class = getattr(chat_module, chat_class_name)

    valid_kwargs = _validate_langchain_args(
        provider, chat_class, class_type="llm", **kwargs
    )
    print(valid_kwargs)
    return LangchainLLMWrapper(chat_class(**valid_kwargs))


def get_embedding_instance(provider: str, **kwargs) -> Tuple[Type, Type]:
    """Return both chat and embedding classes for a given provider."""
    if provider not in PROVIDER_REGISTRY:
        raise ValueError(f"Unknown provider: {provider}")

    (
        pip_package,
        chat_module_path,
        chat_class_name,
        embeddings_module_path,
        embeddings_class_name,
    ) = PROVIDER_REGISTRY[provider]

    try:
        embeddings_module = importlib.import_module(embeddings_module_path)
    except ImportError:
        # In rare cases where chat and embeddings are in separate packages
        # You could adjust pip_package to install multiple things if needed
        print(f"Installing missing package: {pip_package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pip_package])

        embeddings_module = importlib.import_module(embeddings_module_path)

    embeddings_class = getattr(embeddings_module, embeddings_class_name)

    valid_kwargs = _validate_langchain_args(
        provider, embeddings_class, class_type="embedding", **kwargs
    )
    print(valid_kwargs)

    return LangchainEmbeddingsWrapper(embeddings_class(**valid_kwargs))


def get_generator_instance(config_file: str):
    with open(config_file) as f:
        config = json.load(f)
    # Find the pipeline that actually uses RAG (generator = ragas)
    generation_pipeline = next(
        p
        for p in config["generation"]["pipelines"]
        if p.get("generator") == PIPELINE_ID
    )

    # Get target model names for the selected pipeline
    llm_name = generation_pipeline["llm_name"]
    embedding_name = generation_pipeline["embedding_name"]

    # Retrieve llm model details
    llm = next(l_conf for l_conf in config["llms"] if l_conf["name"] == llm_name)
    llm_kwargs = {
        **llm["params"],
        "model": llm["model"],
        "api_key": os.getenv(llm["api_key"]),
        "base_url": llm["base_url"],
    }

    generator_llm = get_llmchat_instance(provider=llm["provider"], **llm_kwargs)

    # Retrieve embedding details
    embedding = next(e for e in config["embeddings"] if e["name"] == embedding_name)
    embedding_kwargs = {
        **embedding["params"],
        "model": embedding["model"],
        "api_key": os.getenv(embedding["api_key"]),
        "base_url": embedding["base_url"],
    }

    generator_embeddings = get_embedding_instance(
        provider=embedding["provider"], **embedding_kwargs
    )

    return TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)


def get_querydistribution_instance(
    config_file: str, llm: LangchainLLMWrapper
) -> QueryDistribution:
    with open(config_file) as f:
        config = json.load(f)

    n_questions = config["generation"]["output"]["max_questions"]
    # Find the pipeline that actually uses RAG (generator = ragas)
    rag_pipeline = next(
        p
        for p in config["generation"]["pipelines"]
        if p.get("generator") == PIPELINE_ID
    )

    dist: QueryDistribution = []

    for item in rag_pipeline["question_distribution"]:
        qtype = item["question_type"]
        # prompt = item["prompt"]
        ratio = item["ratio"]

        SynthClass = QUESTION_SYNTHESIZERS.get(qtype)
        if SynthClass is None:
            raise ValueError(
                f"RAGAS-ERROR: Pipeline {PIPELINE_ID}. Unknown question_type: {qtype}"
            )

        # instantiate the synthesizer with its prompt
        synthesizer = SynthClass(llm=llm)
        dist.append((synthesizer, ratio))

    return n_questions, dist
