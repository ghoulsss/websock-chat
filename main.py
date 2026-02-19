from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.exceptions.auth import TokenNoFoundException, TokenExpiredException
from src.api.v1.auth import router as users_router
from src.api.v1.chat import router as chat_router
from src.api.v1.home import router as home_router
from src.api.v1.socket import router as socket_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")

app.include_router(users_router)
app.include_router(chat_router)
app.include_router(home_router)
app.include_router(socket_router)
