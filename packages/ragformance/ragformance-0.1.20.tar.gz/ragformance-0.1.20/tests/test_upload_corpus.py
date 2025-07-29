from typing import List
import unittest
from ragformance.eval.metrics.trec_eval import trec_eval_metrics
from ragformance.models.answer import (
    AnswerModel,
    AnnotatedQueryModel,
    ReferenceModel,
)
from ragformance.models.corpus import DocModel
from ragformance.rag.naive_rag import NaiveRag


class TestUploadCorpus(unittest.TestCase):
    def test_naive_rag_upload_corpus(self):
        corpus: List[DocModel] = [
            DocModel(
                _id="c_1",
                title="France",
                text="The capital of France is Paris",
            )
        ]

        naive_rag = NaiveRag()
        naive_rag.upload_corpus(corpus=corpus)

        queries: List[AnnotatedQueryModel] = [
            AnnotatedQueryModel(
                _id="q_1",
                query_text="What is the capital of France",
                relevant_document_ids=[ReferenceModel(corpus_id="c_1", score=1)],
                ref_anwser="Paris is the capital of France",
            )
        ]
        naive_rag.ask_queries(queries=queries)
