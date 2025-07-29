from abc import abstractmethod
from pathlib import Path
from typing import Dict

from ragformance.models.answer import AnnotatedQueryModel
from ragformance.models.corpus import DocModel

class QueryGeneratorInterface:
    @abstractmethod
    def generate_synthetic_queries(corpus: list[DocModel], config: Dict = {})-> list[AnnotatedQueryModel]:
        raise NotImplementedError

class AnswerGeneratorInterface:
    @abstractmethod
    def generate_answers(corpus: list[DocModel], queries: list[AnnotatedQueryModel], config: Dict = {}) -> list[AnnotatedQueryModel]:
        raise NotImplementedError

class CorpusGeneratorInterface:
    @abstractmethod
    def generate_corpus(docs_folder: Path, config: Dict = {}) -> list[DocModel]:
        raise NotImplementedError
