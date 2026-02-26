from fastapi import APIRouter, Depends, Response
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.services.auth import AuthService
from src.exceptions.auth import (
    UserAlreadyExistsException,
    IncorrectEmailOrPasswordException,
    PasswordMismatchException,
)
from src.schemas.user import CreateUserSchema, AuthUserSchema

router = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="src/templates")


# @router.get("/", response_class=HTMLResponse, summary="Страница авторизации")
# async def get_auth_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})


@router.post("/register")
async def register_user(
    user_data: CreateUserSchema, auth_service: AuthService = Depends()
) -> dict:
    try:
        result = await auth_service.register_user(user_data)
    except ValueError:
        raise PasswordMismatchException("Пароли не совпадают")
    except Exception:
        raise UserAlreadyExistsException

    return {
        "message": "Вы успешно зарегистрированы!",
        "user": result["user"],
        "access_token": result["access_token"],
    }


@router.post("/login")
async def auth_user(
    user_data: AuthUserSchema, auth_service: AuthService = Depends()
):
    try:
        result = await auth_service.login_user(user_data)
    except IncorrectEmailOrPasswordException:
        raise IncorrectEmailOrPasswordException

    access_token = result["access_token"]

    return {
        "access_token": access_token,
        # "refresh_token": None,
        "user": result["user"],
    }
