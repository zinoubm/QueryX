from fastapi import APIRouter

from app.api import users, utils, queries, documents

api_router = APIRouter()

api_router.include_router(utils.router, tags=["utils"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(queries.router, tags=["queries"])
api_router.include_router(documents.router, tags=["documents"])
