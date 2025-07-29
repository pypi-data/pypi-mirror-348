# RAGFORmance

[![Build status](https://github.com/FOR-sight-ai/RAGFORmance/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/FOR-sight-ai/ragformance/actions)
[![Docs status](https://img.shields.io/readthedocs/RAGFORmance)](TODO)
[![Version](https://img.shields.io/pypi/v/ragformance?color=blue)](https://pypi.org/project/ragformance/)
[![Python Version](https://img.shields.io/pypi/pyversions/ragformance.svg?color=blue)](https://pypi.org/project/ragformance/)
[![Downloads](https://static.pepy.tech/badge/ragformance)](https://pepy.tech/project/ragformance)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/FOR-sight-ai/ragformance/blob/main/LICENSE)

  <!-- Link to the documentation -->
  <a href="TODO"><strong>Explore RAGFORmance docs »</strong></a>
  <br>

</div>

Benchmark for RAG

# Usage

## Using one of the generator
This generators takes of folder of documents, converts them to markdown and generates question using a chain of prompts. It necessitate a LLM (more than 8b parameter is recommended, since the prompts rely on XML output format ).
Data is return and saved to disk in jsonl format.


``` python
from ragformance.data_generation.generators.alpha import run

import subprocess
import json
import os

datapath = "data/DatabaseToloxa"
folder = "1 - Bosch Result"

if not os.path.exists(datapath):
    subprocess.check_call("git","clone", "https://github.com/FOR-sight-ai/DatabaseToloxa.git",datapath)

with open("config.json") as f:
    config = json.load(f)

datapath = os.path.join(datapath, folder)

corpus, queries = run(datapath, output_path = "output",API_KEY=config["LLMkey"], API_URL=config["LLMurl"], API_MODEL=config["LLMmodel"])
```

### Dataset Structure
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
    - `ref_anwser`: The reference answer for the query.
    - `metadata`: A dictionary containing the metadata for the query.


## Pushing dataset to Hugging Face Hub
This function pushes the two jsonl files to a Hugging Face Hub dataset repository; you must set the environment variable HF_TOKEN, either in system environment or config.json

``` python
from ragformance.eval.utils.huggingface_dataloader import push_to_hub
HFpath = "FOR-sight-ai/ragformance-toloxa"
push_to_hub(HFpath, "output")
```


## Using test suite with BEIR datasets 
This functions convert BEIR jsonl data into the internal jsonl format. They are very similar, but BEIR is only for information retrieval task, whereas the library allows other type of evaluations.

``` python
from ragformance.scripts.RAG_abstractions.naive_rag import upload_corpus, ask_queries
from ragformance.eval.utils.beir_dataloader import load_beir_dataset

from ragformance.eval.metrics import trec_eval_metrics
from ragformance.eval.metrics import visualize_semantic_F1, display_semantic_quadrants

import logging
import json

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
with open('config.json','w') as f:
  json.dump({},f)

corpus, queries = load_beir_dataset(filter_corpus = True)

upload_corpus(corpus)
answers = ask_queries(queries[:10])

```

## Metrics and visualization
This library wraps the trev eval tools for Information Retrieval metrics.
It provides also a set metrics visualization to help assess if the test dataset is well balanced and if a solution under test has the expected performances.

```python

metrics = trec_eval_metrics(answers)

quadrants = visualize_semantic_F1(corpus, answers)

display_semantic_quadrants(quadrants)

```

## Example configuration file

``` json
{
    "corpus_text_key": "text"
}


```


## Contributing

Contributions to the Forcolate library are welcome! If you have ideas for new features, improvements, or bug fixes, please open an issue or submit a pull request.

## Acknowledgement

This project received funding from the French ”IA Cluster” program within the Artificial and Natural Intelligence Toulouse Institute (ANITI) and from the "France 2030" program within IRT Saint Exupery. The authors gratefully acknowledge the support of the FOR projects.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
