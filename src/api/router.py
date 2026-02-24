from fastapi import APIRouter

from src.api.v1.auth import router as auth_router
from src.api.v1.chat import router as chat_router
from src.api.v1.home import router as home_router
from src.api.v1.socket import router as socket_router
from src.api.v1.user import router as user_router
from src.core.config import settings

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth_router)
v1_router.include_router(user_router)
v1_router.include_router(chat_router)
v1_router.include_router(home_router)
v1_router.include_router(socket_router)


project_router = APIRouter(prefix=f"/{settings().PROJECT_NAME}")
project_router.include_router(v1_router)

api_router = APIRouter(prefix="/api")
api_router.include_router(project_router)
# api_router.include_router(healthcheck_router)
