from abc import abstractmethod
from pathlib import Path
from typing import List, Optional

from ragformance.models.answer import AnnotatedQueryModel, AnswerModel
from ragformance.models.corpus import DocModel


class RagInterface:

    @abstractmethod
    def upload_corpus(corpus: List[DocModel], config_p: Optional[Path] = None) -> int:
        raise NotImplementedError

    @abstractmethod
    def ask_queries(queries: List[AnnotatedQueryModel], config_p: Optional[Path] = None) -> List[AnswerModel]:
        raise NotImplementedError
