from typing import Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from starlette.responses import Response
from app.schemas.document import UpsertResponse
from app.parser.parser import get_document_from_file
from app.parser.chunk import chunk_text
import requests

from app.deps.users import current_user
from app.models.user import User
from app.parser.parser import get_document_from_file
from sqlalchemy.ext.asyncio.session import AsyncSession
from app.deps.db import get_async_session

from app.models.document import Document
from uuid import uuid4

from app.vectorstore.qdrant import QdrantManager
from app.openai.base import OpenAiManager
from sqlalchemy.future import select


router = APIRouter(prefix="/documents")


@router.post(
    "/upsert-file",
    response_model=UpsertResponse,
)
async def upsert_file(
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    document = await get_document_from_file(file)
    chunks = chunk_text(document.text, max_size=2000)
    db_document = Document(user_id=str(user.id).replace("-", ""), name=file.filename)
    session.add(db_document)

    await session.commit()

    openai_manager = OpenAiManager()
    ids = [uuid4().hex for chunk in chunks]
    payloads = [
        {
            "user_id": str(user.id).replace("-", ""),
            "document_id": db_document.id,
            "chunk": chunk,
        }
        for chunk in chunks
    ]
    embeddings = openai_manager.get_embeddings(chunks)

    vector_manager = QdrantManager()
    response = vector_manager.upsert_points(ids, payloads, embeddings)

    return UpsertResponse(id=db_document.id)


@router.get("/")
async def get_documents(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    statement = select(Document).where(
        Document.user_id == str(user.id).replace("-", "")
    )
    db_documents = await session.execute(statement)

    documents = [
        {"id": document.id, "name": document.name}
        for document in db_documents.scalars().all()
    ]

    return {"documents": documents}
