from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from core.config import settings

middleware = [
    Middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=settings().CORS_ALLOW_ORIGIN_LIST,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]
