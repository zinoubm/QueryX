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

    embedding = [list(range(1, 1536))]

    db_document = Document(user_id=user.id, name=file.filename)

    session.add(db_document)

    await session.commit()

    document_chunks = []

    # for chunk, embedding in zip(chunks, embeddings):
    for chunk in chunks:
        document_chunk = {
            "id": uuid4().hex,
            "text": chunk,
            "embedding": embedding,
        }

        document_chunks.append(document_chunk)

    ids = [chunk["id"] for chunk in document_chunks]
    payloads = [{"chunk": chunk["text"]} for chunk in document_chunks]
    embeddings = [chunk["embedding"] for chunk in document_chunks]
    # response = vector_manager.upsert_points(record_ids, record_payloads, record_embeddings)
    vector_manager = QdrantManager()
    response = vector_manager.upsert_points(ids, payloads, embeddings)

    print(
        {
            "file_name": file.filename,
            "user_id": user.id,
            # "document": document,
            "lenght": len(chunks),
            "chunks": ids,
        }
    )
    return UpsertResponse(id=db_document.id)
