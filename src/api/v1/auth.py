from fastapi import APIRouter, Depends, HTTPException

from services.auth import AuthService
from exceptions.auth import (
    UserAlreadyExistsException,
    IncorrectEmailOrPasswordException,
    PasswordMismatchException,
)
from schemas.user import CreateUserSchema, AuthUserSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


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
async def auth_user(user_data: AuthUserSchema, auth_service: AuthService = Depends()):
    try:
        result = await auth_service.login_user(user_data)
    except IncorrectEmailOrPasswordException:
        # raise IncorrectEmailOrPasswordException
        raise HTTPException(
            status_code=401,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = result["access_token"]

    return {
        "access_token": access_token,
        "user": result["user"],
    }
