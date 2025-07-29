from typing import List
import unittest
from ragformance.eval.metrics.trec_eval import trec_eval_metrics
from ragformance.models.answer import (
    AnswerModel,
    AnnotatedQueryModel,
    RelevantDocumentModel,
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
        doc_uploaded_num = naive_rag.upload_corpus(corpus=corpus)
        assert doc_uploaded_num == 1

