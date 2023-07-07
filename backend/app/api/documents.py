from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response
import requests


from app.deps.users import current_user
from app.models.user import User

from app.vectorstore.qdrant import VectorClient
from app.schemas.query import Query

router = APIRouter(prefix="/documents")
