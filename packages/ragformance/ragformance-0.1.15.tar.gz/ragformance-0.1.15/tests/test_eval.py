import json
import unittest
from ragformance.eval.metrics.trec_eval import trec_eval_metrics
from ragformance.models.answer import (
    AnswerModel,
    AnnotatedQueryModel,
    ReferenceModel,
)


class TestEval(unittest.TestCase):
    def test_sim(self):
        answers = [
            AnswerModel(
                _id="a_1",
                query=AnnotatedQueryModel(
                    _id="q_1",
                    text="What is the capital of France",
                    references=[ReferenceModel(corpus_id="c_1", score=1)],
                    ref_anwser="Paris is the capital of France",
                ),
                text="Paris",
                relevant_documents_ids=["c_1"],
            )
        ]

        json_answers = [a.model_dump(by_alias=True) for a in answers]

        ndcg, _map, recall, precision = trec_eval_metrics(json_answers)

        assert ndcg["NDCG@1"] == 1.0 and _map["MAP@1"] == 1.0
