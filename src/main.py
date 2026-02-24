from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.api.router import v1_router
from src.core.config import settings
from src.exceptions.auth import TokenNoFoundException, TokenExpiredException
from src.core.middlewares import middleware

app = FastAPI(
    title=settings().PROJECT_NAME,
    # openapi_url="/api/openapi.json",
    docs_url="/api/swagger",
    middleware=middleware,
    # swagger_ui_parameters={"operationsSorter": "method"},
)

app.include_router(v1_router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app", host=settings().SERVER_HOST, port=settings().SERVER_PORT, workers=settings().SERVER_WORKERS_COUNT
#     )
