"""
RAGformance End-to-End Runner

This module allows you to run the full pipeline for question generation, upload, evaluation, metrics computation, and visualization
for RAG datasets, either from the command line or as a Python library.
Each step is controlled by flags in the JSON configuration file.

CLI usage:
    ragformance --config config.json

Example config.json structure:
{
    "data_path": "data/",
    "model_path": "output/",
    "log_path": "logs/",
    "raw_data_folder": "scifact/",
    "generator_type": "alpha",
    "rag_type": "naive",
    "hf_path": "FOR-sight-ai/ragformance-test",
    "steps": {
        "generation": true,
        "upload_hf": true,
        "evaluation": true,
        "metrics": true,
        "visualization": true
    }
}
"""

import os
import json
import logging
import argparse
from typing import List
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel
from pydantic import TypeAdapter


# load config file
def load_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    return config


# set up logging
def setup_logging(log_path):
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.info("Logging setup complete.")


def run_pipeline(config_path="config.json"):
    """
    Run the full or partial pipeline according to the steps enabled in the config.
    """
    config = load_config(config_path)
    log_path = config["log_path"]
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    setup_logging(log_path + "/ragformance.log")

    steps = config.get("steps", {})
    model_path = config["model_path"]
    log_path = config["log_path"]

    corpus: List[DocModel] = []
    queries: List[AnnotatedQueryModel] = []
    # answers: List[AnswerModel] = []

    ta = TypeAdapter(List[DocModel])
    taq = TypeAdapter(List[AnnotatedQueryModel])

    # Question generation
    if steps.get("generation", True):
        logging.info("[STEP] Question generation.")
        generator = config.get("generation", {})
        generator_type = generator.get("type", None)
        data_path = generator.get("source", {}).get("path", None)
        output_path = generator.get("output", {}).get("path", None)

        llms = config.get("LLMs", None)
        if llms is None:
            logging.error("LLMs not set in config. Please set LLMs in the config file.")
            generator_type = None
        else:
            apikey = llms[0].get("api_key", None)
            model = llms[0].get("model", None)
            url = llms[0].get("base_url", None)

        # selecting the generator
        if generator_type == "alpha":
            from ragformance.generators.alpha import run as run_alpha

            corpus, queries = run_alpha(
                data_path,
                output_path=output_path,
                API_KEY=apikey,
                API_URL=url,
                API_MODEL=model,
            )

        elif generator_type == "aida":
            from ragformance.generators.aida import run as run_aida

            corpus, queries = run_aida(
                seed_questions_path=os.path.join(data_path, "seed_questions.json"),
                data_dir=data_path,
                output_dir=output_path,
                openrouter_key=apikey,
                openrouter_base_url=url,
                hf_embed_model=config.get("embeddings", [])[0].get("model", None),
                capella_path=os.path.join(data_path, "data.capella"),
                entity_model_name=llms[1].get("model", model),
                qa_model_name=model,
            )
        elif generator_type == "based_llm_and_summary":
            os.environ["OPENAI_API_KEY"] = apikey
            os.environ["OPENAI_BASE_URL"] = url
            os.environ["OPENAI_SUMMARY_MODEL"] = llms[1].get("model", model)
            os.environ["OPENAI_QA_MODEL"] = model

            from ragformance.generators.based_llm_and_summary import run as run_bls

            corpus, queries = run_bls(data_path, output_path)
        elif generator_type == "error_code":
            from ragformance.generators.error_code import run as run_error_code

            corpus, queries = run_error_code(
                data_path,
                prefix_id="ELE",
                title="Manuel utilisateur machine à laver Electrolux WAL7E300",
                API_KEY=apikey,
                API_URL=url,
                API_MODEL=model,
            )

        else:
            raise ValueError(f"Unknown generator type: {generator_type}")
        corpus, queries = generator.generate_data(config)
        logging.info("Data generation complete.")

    # Upload to HuggingFace
    if steps.get("upload_hf", False):
        logging.info("[STEP] HuggingFace upload.")
        from ragformance.dataloaders import push_to_hub

        hf_path = config.get("hf", {}).get("hf_path", None)
        data_path = config.get("generation", {}).get("output", {}).get("path", None)
        hf_token = config.get("hf", {}).get("hf_token", None)
        if hf_path and data_path:
            push_to_hub(
                hf_path, data_path, hf_token
            )  # Note : we could wrap other parameters from config, but we focus on the main ones to have uniform pipelines
            logging.info("[UPLOAD] Upload complete.")
        else:
            logging.info("[UPLOAD] hf.hf_path or generation.output.path not set.")

    # Load dataset from source
    if steps.get("load_dataset", False):
        logging.info("[STEP] Loading dataset from source enabled.")
        if len(corpus) > 0 or len(queries) > 0:
            logging.warning(
                "[Warning] Dataset already loaded from generation. Loading will replace the current dataset."
            )

        source_type = config.get("dataset", {}).get("source_type", "jsonl")
        source_path = config.get("dataset", {}).get("path", "")

        if source_type == "jsonl":
            with open(os.path.join(source_path, "corpus.jsonl")) as f:
                corpus = ta.validate_python([json.loads(line) for line in f])
            with open(os.path.join(source_path, "queries.jsonl")) as f:
                queries = taq.validate_python([json.loads(line) for line in f])

        elif source_type == "huggingface":
            from datasets import load_dataset

            corpus = ta.validate_python(
                load_dataset(source_path, "corpus", split="train")
            )
            queries = taq.validate_python(
                load_dataset(source_path, "queries", split="train")
            )
        elif source_type == "beir":
            from ragformance.dataloaders import load_beir_dataset

            corpus, queries = load_beir_dataset(dataset=source_path)

    # RAG evaluation
    if steps.get("evaluation", True):
        logging.info("[STEP] RAG evaluation enabled.")
        run_pipeline_evaluation(config)

    # Metrics computation
    if steps.get("metrics", True):
        logging.info("[STEP] Metrics computation enabled.")
        compute_metrics(config)

    # Visualization
    if steps.get("visualization", True):
        logging.info("[STEP] Visualization enabled.")
        run_visualization(config)

    # Save status
    results_path = os.path.join(model_path, "results.json")
    with open(results_path, "w") as f:
        json.dump({"status": "success"}, f)
    logging.info("Results saved.")


def main():
    parser = argparse.ArgumentParser(description="RAGformance End-to-End Runner")
    parser.add_argument(
        "--config", type=str, required=True, help="Path to config JSON file"
    )
    args = parser.parse_args()

    run_pipeline(args.config)


def get_rag_class(config):
    rag_type = config.get("rag_type", "naive")
    if rag_type == "naive":
        from ragformance.rag.naive_rag import NaiveRag

        return NaiveRag()
    elif rag_type == "openwebui":
        from ragformance.rag.openwebui_rag import OpenwebuiRag

        return OpenwebuiRag()
    else:
        raise ValueError(f"Unknown rag_type: {rag_type}")


def run_pipeline_evaluation(config):
    logging.info("[EVALUATION] Starting RAG evaluation...")
    rag = get_rag_class(config)
    from ragformance.models.corpus import DocModel
    from ragformance.models.answer import AnnotatedQueryModel
    import pandas as pd

    data_path = config["data_path"]
    corpus_path = os.path.join(data_path, "corpus.jsonl")
    queries_path = os.path.join(data_path, "queries.jsonl")
    corpus = [
        DocModel(**d)
        for d in pd.read_json(corpus_path, lines=True).to_dict(orient="records")
    ]
    queries = [
        AnnotatedQueryModel(**q)
        for q in pd.read_json(queries_path, lines=True).to_dict(orient="records")
    ]
    rag.upload_corpus(corpus, config)
    rag.ask_queries(queries, config)
    logging.info("[EVALUATION] RAG evaluation complete.")


def compute_metrics(config):
    logging.info("[METRICS] Computing metrics...")
    from ragformance.eval.metrics import evaluate

    data_path = config["data_path"]
    model_path = config["model_path"]
    evaluate(data_path, model_path)
    logging.info("[METRICS] Metrics computation complete.")


def run_visualization(config):
    logging.info("[VISUALIZATION] Generating visualizations...")
    # To be adapted to your visualization logic
    # For example: from ragformance.visualization import generate_report
    # generate_report(config)
    logging.info("[VISUALIZATION] Visualization complete.")


if __name__ == "__main__":
    main()
