from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response
import requests


from app.deps.users import current_user
from app.models.user import User

# from app.vectorstore.qdrant import VectorClient
# from app.schemas.query import Query

from app.vectorstore.qdrant import QdrantManager
from app.openai.base import OpenAiManager
from app.openai.core import ask, summarize

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str
    document_id: str


class QueryResponse(BaseModel):
    answer: str
    document_id: str


router = APIRouter(prefix="/queries")


@router.post("/")
async def query(
    query_request: QueryRequest,
    response: Response,
    user: User = Depends(current_user),
) -> QueryResponse:
    if user:
        # print("wow")
        vector_client = QdrantManager()
        openai_client = OpenAiManager()
        query_embedding = openai_client.get_embedding(query_request.query)
        points = vector_client.search_point(
            query_embedding, user.id, query_request.filename, limit=3
        )
        # answer = ask(points, query_request.query, openai_client)
    else:
        raise Exception

    # query_response = QueryResponse(answer=answer, filename=query_request.filename)
    query_response = QueryResponse(answer="wow", filename="wow.pdf")

    return query_response


# @router.get("/{query}")
# async def query(
#     query: str,
#     response: Response,
#     user: User = Depends(current_user),
# ) -> Any:
#     if user:
#         client = VectorClient()
#         answer = client.answer(query)

#     else:
#         raise Exception

#     return {"answer": answer}
