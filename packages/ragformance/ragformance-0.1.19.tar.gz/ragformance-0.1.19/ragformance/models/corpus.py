
from typing import List, Optional
from pydantic import BaseModel

class CorpusModel(BaseModel):
    _id: str
    title: str
    text: str

