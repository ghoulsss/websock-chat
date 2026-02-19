from fastapi import Request, HTTPException, APIRouter
from starlette.responses import RedirectResponse

from src.exceptions.auth import TokenExpiredException, TokenNoFoundException
from src.db.session import test_db

router = APIRouter(prefix="/home", tags=["home"])


@router.get("/health")
async def health():
    return await test_db()


@router.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")
