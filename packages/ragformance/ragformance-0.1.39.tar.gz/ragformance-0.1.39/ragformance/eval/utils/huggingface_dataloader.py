from huggingface_hub import login
from datasets import load_dataset
import os
import json


# package and upload to huggingface
def push_to_hub(HFpath, folderpath):
    HF_TOKEN = ""
    if os.environ.get("HF_TOKEN") is None:
        with open("config.json") as f:
            config = json.load(f)
        HF_TOKEN = config["HF_TOKEN"]
    else:
        HF_TOKEN = os.environ["HF_TOKEN"]

    login(token=HF_TOKEN)
    corpuspath = os.path.join(folderpath, "corpus.jsonl")
    queriespath = os.path.join(folderpath, "queries.jsonl")

    dataset = load_dataset(
        "json",
        data_files=corpuspath,
        split="train",
    )
    dataset.push_to_hub(HFpath, "corpus", private=True)

    datasetqueries = load_dataset("json", data_files=queriespath, split="train")
    datasetqueries.push_to_hub("HFpath", "queries")

    from huggingface_hub.repocard import RepoCard

    card = RepoCard.load(HFpath, repo_type="dataset")

    card.text = """
    # RAGformance Dataset
    This is a dataset for evaluating RAG models generated with RAGFORmande. The dataset contains a set of queries and a corpus of documents. The queries are designed to test the performance of RAG models on a specific dataset with questions generated syntheticallly.


    ## Dataset Structure
    The dataset consists of two files:
    - `corpus.jsonl`: A jsonl file containing the corpus of documents. Each document is represented as a json object with the following fields:
        - `_id`: The id of the document.
        - `title`: The title of the document.
        - `text`: The text of the document.
    - `queries.jsonl`: A jsonl file containing the queries. Each query is represented as a json object with the following fields:
        - `_id`: The id of the query.
        - `text`: The text of the query.
        - `references`: A list of references to the documents in the corpus. Each reference is represented as a json object with the following fields:
            - `corpus_id`: The id of the document.
            - `score`: The score of the reference.
        - `ref_answer`: The reference answer for the query.
        - `metadata`: A dictionary containing the metadata for the query.


    [RAGFORmance library](https://github.com/FOR-sight-ai/ragformance)

    ## Acknowledgement

    This project received funding from the French ”IA Cluster” program within the Artificial and Natural Intelligence Toulouse Institute (ANITI) and from the "France 2030" program within IRT Saint Exupery. The authors gratefully acknowledge the support of the FOR projects.

    ## License
    This dataset is licensed under the MIT license. See the LICENSE file for more details.
    """
    card.push_to_hub(HFpath, repo_type="dataset")
