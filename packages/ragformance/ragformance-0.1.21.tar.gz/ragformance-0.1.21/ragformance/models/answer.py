
from typing import List, Optional
from pydantic import BaseModel, Field


class ReferenceModel(BaseModel):
    corpus_id: str
    score: int

class AnnotatedQueryModel(BaseModel):
    id: str = Field(alias="_id")
    query_text: str
    
    relevant_document_ids: List[ReferenceModel]
    ref_anwser: str

class AnswerModel(BaseModel):
    id: str = Field(alias="_id")
    
    query: AnnotatedQueryModel

    # model output
    model_answer: str
    retrieved_documents_ids: List[str]
    retrieved_documents_distances: List[float]

    