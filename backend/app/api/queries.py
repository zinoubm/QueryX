from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response
import requests


from app.deps.users import current_user
from app.models.user import User

from app.vectorstore.qdrant import VectorClient
from app.schemas.query import Query

router = APIRouter(prefix="/queries")


@router.get("/{query}")
async def query(
    query: str,
    response: Response,
    user: User = Depends(current_user),
) -> Any:
    if user:
        client = VectorClient()
        answer = client.answer(query)

    else:
        raise Exception

    return {"answer": answer}
