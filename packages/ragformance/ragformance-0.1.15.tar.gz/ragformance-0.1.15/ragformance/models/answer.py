
from typing import List, Optional
from pydantic import BaseModel, Field


class ReferenceModel(BaseModel):
    corpus_id: str
    score: int

class AnnotatedQueryModel(BaseModel):
    id: str = Field(alias="_id")
    text: str
    
    references: List[ReferenceModel]
    ref_anwser: str

class AnswerModel(BaseModel):
    id: str = Field(alias="_id")
    
    query: AnnotatedQueryModel

    # model output
    text: str
    relevant_documents_ids: List[str]

    