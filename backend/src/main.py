from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

from api.router import api_router
from core.config import settings
from exceptions.auth import TokenNoFoundException, TokenExpiredException
from core.middlewares import middleware
import uvicorn


app = FastAPI(
    title=settings().PROJECT_NAME,
    docs_url="/api/swagger",
    middleware=middleware,
)

app.include_router(api_router)


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings().SERVER_HOST,
        port=settings().SERVER_PORT,
        workers=settings().SERVER_WORKERS_COUNT,
    )
