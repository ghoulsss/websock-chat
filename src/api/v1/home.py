from fastapi import Request, HTTPException, APIRouter
from starlette.responses import RedirectResponse

from src.exceptions.auth import TokenExpiredException, TokenNoFoundException
from src.db.session import test_db

router = APIRouter(prefix="/")


@router.get("/health")
async def health():
    return await test_db()


@router.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@router.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")


@router.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/auth")
