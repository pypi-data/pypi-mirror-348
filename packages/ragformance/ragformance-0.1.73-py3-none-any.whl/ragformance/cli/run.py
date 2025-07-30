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

    corpus = []
    queries = []

    # Question generation
    if steps.get("generation", True):
        logging.info("[STEP] Question generation enabled.")
        generator_type = config["generator_type"]

        if generator_type == "alpha":
            from ragformance.generators.generators import AlphaQA

            generator = AlphaQA(config)
        elif generator_type == "beta":
            from ragformance.generators.generators import BetaQA

            generator = BetaQA(config)
        else:
            raise ValueError(f"Unknown generator type: {generator_type}")
        corpus, queries = generator.generate_data(config)
        logging.info("Data generation complete.")

    # Upload to HuggingFace
    if steps.get("upload_hf", False):
        logging.info("[STEP] HuggingFace upload enabled.")
        upload_to_huggingface(config, corpus, queries)

    # Load dataset from source
    if steps.get("load_dataset", False):
        logging.info("[STEP] Loading dataset from source enabled.")

        source_type = config.get("source_type", "json")
        if source_type == "jsonl":
            from ragformance.generators.load_dataset import load_jsonl_dataset

            load_jsonl_dataset(config)
        elif source_type == "huggingface":
            from ragformance.generators.load_dataset import (
                load_huggingface_dataset,
            )

            load_huggingface_dataset(config)
        elif source_type == "beir":
            from ragformance.generators.load_dataset import load_beir_dataset

            load_beir_dataset(config)

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


def upload_to_huggingface(config):
    logging.info("[UPLOAD] Uploading corpus to HuggingFace...")
    from ragformance.eval.utils.huggingface_dataloader import push_to_hub

    hf_path = config.get("hf_path", "FOR-sight-ai/ragformance-test")
    data_path = config["data_path"]
    push_to_hub(hf_path, data_path)
    logging.info("[UPLOAD] Upload complete.")


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
