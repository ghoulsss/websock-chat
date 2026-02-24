from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.core.config import settings


middleware = []

if settings().USE_CORS_MIDDLEWARE:
    middleware.append(
        Middleware(
            CORSMiddleware,
            allow_credentials=True,
            allow_origins=settings().CORS_ALLOW_ORIGIN_LIST,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    )
