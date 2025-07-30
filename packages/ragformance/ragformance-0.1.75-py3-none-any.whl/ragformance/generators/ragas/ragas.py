from ragformance.data_generation.generators.ragas.ragas_setup import (
    get_generator_instance,
    get_querydistribution_instance,
)
from langchain_community.document_loaders import DirectoryLoader
from ragas.testset.synthesizers.generate import TestsetGenerator
from ragas.testset.graph import NodeType

import os
import inspect
import json
import uuid
import sys


def _validate_input_files(datapath):
    # Validate directory contents
    try:
        files = os.listdir(datapath)
    except FileNotFoundError:
        print(f"Error: The directory '{datapath}' does not exist.")
        sys.exit(1)

    valid_files = [f for f in files if f.lower().endswith((".txt", ".md"))]

    if not valid_files:
        print(
            f"Error: No .txt or .md files found in '{datapath}'. Please provide at least one valid file."
        )
        sys.exit(1)

    print("Files to be processed:")
    for f in valid_files:
        print(f" - {f}")

    return True


def _validate_additional_arguments(**kwargs):
    # Get the signature of the method
    sig = inspect.signature(TestsetGenerator.generate)

    # Get arguments from the method TestsetGenerator.generate
    valid_arg_names = [
        name
        for name in sig.parameters
        if name != "self"  # usually omit 'self'
    ]

    # Find any unexpected arguments on **kwargs
    unexpected_args = [key for key in kwargs if key not in valid_arg_names]

    if unexpected_args:
        raise ValueError(
            f"Unexpected argument(s): {', '.join(unexpected_args)}. "
            f"Valid arguments are: {', '.join(sorted(valid_arg_names))}"
        )

    # Optionally: return True if all is valid (not necessary, but helpful for chaining)
    return True


def _relationship_condition(rel):
    # Define your condition as a lambda
    return rel.type == "child"


def _extract_corpus_items(kg):
    corpus_items = []

    # The corpus will be formed only by the chunks of the ragas knowledge graph

    # Define your condition as a lambda
    relationship_condition = _relationship_condition

    # Then, call your function with this condition:
    result = kg.find_two_nodes_single_rel(relationship_condition)

    for node_a, rel, node_b in result:
        for node in [node_a, node_b]:
            if getattr(node, "type", None) == NodeType.CHUNK:
                # Assume 'page_content' is the property where the string might be present
                corpus_text = getattr(node, "properties", {}).get("page_content", "")
                corpus_id = str(node.id)
            if getattr(node, "type", None) == NodeType.DOCUMENT:
                corpus_title = (
                    getattr(node, "properties", {})
                    .get("document_metadata", "")
                    .get("source", "")
                )
        corpus_items.append(
            {"_id": corpus_id, "title": corpus_title, "text": corpus_text}
        )

    return corpus_items


def _extract_chunk_id(chunk_str, kg):
    chunk_id = None

    # Define your condition as a lambda
    relationship_condition = _relationship_condition

    # Then, call your function with this condition:
    result = kg.find_two_nodes_single_rel(relationship_condition)

    search_str = chunk_str[:30]

    for node_a, rel, node_b in result:
        # node_a is always of type CHUNK based on your output, but let's check both just in case
        for node in [node_a, node_b]:
            if getattr(node, "type", None) == NodeType.CHUNK:
                # Assume 'page_content' is the property where the string might be present
                page_content = getattr(node, "properties", {}).get("page_content", "")
                if search_str in page_content:
                    chunk_id = str(node.id)
                    break
        if chunk_id is not None:
            break

    return chunk_id


def run(
    config_file=None,
    datapath=None,
    output_path=None,
    ragas_generator=None,
    n_questions=None,
    save_ragas_kg=True,
    **kwargs,
):
    # Collect non-default argument names and values
    others = {
        k: v
        for k, v in [
            ("datapath", datapath),
            ("output_path", output_path),
            ("ragas_generator", ragas_generator),
            ("n_questions", n_questions),
            ("save_ragas_kg", save_ragas_kg),
            *kwargs.items(),
        ]
        if v is not None
        and k
        != "save_ragas_kg"  # (if save_ragas_kg default True is considered "not provided")
    }

    if config_file and others:
        raise ValueError(
            "Provide either 'config_file' only OR other arguments (excluding 'config_file'), not both."
        )

    if not config_file and not others:
        raise ValueError(
            "You must provide either 'config_file' OR other arguments (excluding 'config_file')."
        )

    # Validate run function calling

    if config_file:
        with open(config_file) as f:
            config = json.load(f)
        datapath = config["generation"]["source"]["path"]
        output_path = config["generation"]["output"]["path"]
        ragas_generator = get_generator_instance(config_file)
        n_questions, ragas_querydistribution = get_querydistribution_instance(
            config_file, llm=ragas_generator.llm
        )
    else:
        # Chek testsetgenerator is correctly instantiated
        if not isinstance(ragas_generator, TestsetGenerator):
            raise TypeError(
                f"Argument 'generator' must be a TestsetGenerator, not {type(TestsetGenerator)}"
            )

        # Check **kwargs comply with TestsetGenerator.generate method.
        _validate_additional_arguments(**kwargs)

        # Check n_questions value
        if not n_questions:
            raise TypeError(
                "Argument 'n_questions' must be set (positive integer > 0 )"
            )

    # Check the document corpus (must contain only .txt or .md documents)
    _validate_input_files(datapath)
    # Load docs, only .txt of .md
    loader = DirectoryLoader(datapath, glob=["**/*.txt", "**/*.md"])
    docs = loader.load()

    dataset = ragas_generator.generate_with_langchain_docs(
        docs, testset_size=n_questions
    )
    if save_ragas_kg:
        path = os.path.join(output_path, "knowledge_graph_ragas.json")
        ragas_generator.knowledge_graph.save(path)

    query_items = []

    for data_item in dataset.to_list():
        # query item
        query_item = {
            "_id": str(uuid.uuid4()),  # or doc.id depending on the implementation
            "text": data_item["user_input"],
            "ref_answer": data_item["reference"],
            "references": [
                {
                    "corpus_id": _extract_chunk_id(
                        chunk_str=context, kg=ragas_generator.knowledge_graph
                    ),
                    "score": 1.0,
                }
                for context in data_item["reference_contexts"]
            ],
            "metadata": {"synthesizer_name": data_item["synthesizer_name"]},
        }
        query_items.append(query_item)

    corpus_items = _extract_corpus_items(kg=ragas_generator.knowledge_graph)

    corpus_path = os.path.join(output_path, "corpus.jsonl")
    queries_path = os.path.join(output_path, "queries.jsonl")

    # save corpus and queries to json lines files

    # Ensure the folder exists
    os.makedirs(os.path.dirname(corpus_path), exist_ok=True)
    with open(corpus_path, "w") as f:
        for line in corpus_items:
            f.write(json.dumps(line) + "\n")

    # Ensure the folder exists
    os.makedirs(os.path.dirname(queries_path), exist_ok=True)
    with open(queries_path, "w") as f:
        for line in query_items:
            f.write(json.dumps(line) + "\n")

    return corpus_items, query_items
