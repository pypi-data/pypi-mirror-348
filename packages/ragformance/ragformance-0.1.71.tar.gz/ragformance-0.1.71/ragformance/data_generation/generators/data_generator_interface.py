from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional
from ragformance.models.answer import AnnotatedQueryModel
from ragformance.models.corpus import DocModel

class QueryGeneratorInterface(ABC):
    @abstractmethod
    def generate_synthetic_queries(
        self, corpus: list[DocModel], config: Dict = {}
    ) -> list[AnnotatedQueryModel]:
        raise NotImplementedError

class AnswerGeneratorInterface(ABC):
    @abstractmethod
    def generate_answers(
        self,
        corpus: list[DocModel],
        queries: list[AnnotatedQueryModel],
        config: Dict = {},
    ) -> list[AnnotatedQueryModel]:
        raise NotImplementedError

class CorpusGeneratorInterface(ABC):
    @abstractmethod
    def generate_corpus(self, docs_folder: Path, config: Optional[Dict] = None) -> list[DocModel]:
        raise NotImplementedError
