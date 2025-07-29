from abc import abstractmethod
from typing import Dict, List

from ragformance.models.answer import AnnotatedQueryModel, AnswerModel
from ragformance.models.corpus import DocModel


class RagInterface:
    @abstractmethod
    def upload_corpus(corpus: List[DocModel], config: Dict = {}) -> int:
        raise NotImplementedError

    @abstractmethod
    def ask_queries(
        queries: List[AnnotatedQueryModel], config: Dict = {}
    ) -> List[AnswerModel]:
        raise NotImplementedError
