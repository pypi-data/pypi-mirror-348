from typing import Dict
from pydantic import BaseModel, Field


class DocModel(BaseModel):
    id: str = Field(alias="_id")
    title: str
    text: str
    metadata: Dict
