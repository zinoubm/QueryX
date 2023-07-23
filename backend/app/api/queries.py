from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response
import requests


from app.deps.users import current_user
from app.models.user import User

from app.vectorstore.qdrant import qdrant_manager
from app.openai.base import openai_manager
from app.openai.core import ask, summarize

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    document_id: int


class QueryResponse(BaseModel):
    answer: str
    document_id: int


router = APIRouter(prefix="/queries")


@router.post("/")
async def query(
    query_request: QueryRequest,
    response: Response,
    user: User = Depends(current_user),
) -> QueryResponse:
    query_vector = openai_manager.get_embedding(query_request.query)
    print("user_id type: ")
    print(type(user.id.hex))
    points = qdrant_manager.search_point(
        query_vector=query_vector,
        user_id=user.id.hex,
        document_id=query_request.document_id,
        limit=10,
    )

    answer = ask(
        "\n\n\n".join([point.payload["chunk"] for point in points]),
        query_request.query,
        openai_manager,
    )

    print("answer: ->")
    print(answer)

    query_response = QueryResponse(answer=answer, document_id=query_request.document_id)

    return query_response
