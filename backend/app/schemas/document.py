from pydantic import BaseModel
from typing import List, Optional


class Document(BaseModel):
    id: Optional[str] = None
    text: str


class UpsertRequest(BaseModel):
    documents: List[Document]


class UpsertResponse(BaseModel):
    id: str
