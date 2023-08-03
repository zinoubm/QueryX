from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response
import requests


from app.deps.users import current_user
from app.models.user import User

from app.vectorstore.qdrant import qdrant_manager
from app.openai.base import openai_manager
from app.openai.core import ask, filter, summarize

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
    # add check that this user actually owns this document

    query_vector = openai_manager.get_embedding(query_request.query)

    # print(">>>>>>>>>>>>")
    # print("query vector")
    # print(query_vector)

    # print(">>>>>>>>>>>>>>>")
    # print("document_id: ", query_request.document_id)
    # print("--------------")

    # print(">>>>>>>>>>>>")
    # print("user_id")
    # print(user.id.hex)

    points = qdrant_manager.search_point(
        query_vector=query_vector,
        user_id=str(user.id.hex),
        document_id=int(query_request.document_id),
        limit=1000,
    )

    # print(">>>>>>>>>>>>")
    # print("points")
    # print(points)

    context = "\n\n\n".join([point.payload["chunk"] for point in points])
    # print(">>>>>>>>>>>>")
    # print("context")
    # print(context)

    # filter_response = filter(context, query_request.query, openai_manager)
    # print(">>>>>>>>>>>>>>>>")
    # print("filter resopnse")
    # print(filter_response)
    # print("----------------")
    # remove later
    filter_response = True
    if filter_response:
        answer = ask(
            context,
            query_request.query,
            openai_manager,
        )

        query_response = QueryResponse(
            answer=answer, document_id=query_request.document_id
        )

    else:
        query_response = QueryResponse(
            answer="Sorry, Your question is out of Context!",
            document_id=query_request.document_id,
        )

    return query_response
