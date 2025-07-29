import os
import json
import logging


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


# set up paths
def setup_paths(config):
    # Set up paths for data, models, and logs
    data_path = config["data_path"]
    model_path = config["model_path"]
    log_path = config["log_path"]

    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    return data_path, model_path, log_path


# run the pipeline
def run_pipeline(config, data_path, model_path, log_path):
    # load the raw data based on config file
    logging.info("Loading raw data...")
    raw_data_path = os.path.join(data_path, config["raw_data_folder"])

    # call the Q&A generator based on the generator type in the config file
    generator_type = config["generator_type"]
    if generator_type == "alpha":
        from ragformance.data_generation.generators import AlphaQA

        generator = AlphaQA(config)
    elif generator_type == "beta":
        from ragformance.data_generation.generators import BetaQA

        generator = BetaQA(config)
    else:
        raise ValueError(f"Unknown generator type: {generator_type}")

    # generate the data
    logging.info("Generating data...")
    generator.generate_data(raw_data_path, data_path)
    logging.info("Data generation complete.")

    # optional : run a local RAG process as a separate thread, wait for it to be ready
    if config["rag_local"]:
        logging.info("Starting local RAG process...")
        from ragformance.scripts.RAG_abstractions import start_rag_process

        start_rag_process(config)
        logging.info("Local RAG process started.")

    # upload the corpus dataset to the RAG collection endpoint
    logging.info("Uploading corpus dataset to RAG collection endpoint...")

    from ragformance.scripts.RAG_abstractions import upload_corpus

    upload_corpus(data_path, config)
    logging.info("Corpus dataset upload complete.")

    # run the RAG pipeline on each question in the question dataset
    logging.info("Running RAG pipeline...")
    from ragformance.scripts.RAG_abstractions import run_rag_pipeline

    run_rag_pipeline(data_path, model_path, config)
    logging.info("RAG pipeline complete.")

    # run the evaluation pipeline
    logging.info("Running evaluation pipeline...")
    from ragformance.eval.metrics import evaluate

    evaluate(data_path, model_path)
    logging.info("Evaluation pipeline complete.")
    # save the results
    logging.info("Saving results...")
    results_path = os.path.join(model_path, "results.json")
    with open(results_path, "w") as f:
        json.dump({"status": "success"}, f)
    logging.info("Results saved.")
