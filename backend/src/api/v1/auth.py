from fastapi import APIRouter, Depends, HTTPException

from schemas.auth import LoginUserSchema, RegisterUserSchema
from services.auth import AuthService
from fastapi import status
from schemas.user import CreateUserSchema, AuthUserSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=RegisterUserSchema)
async def register_user(
    user_data: CreateUserSchema, auth_service: AuthService = Depends()
)-> RegisterUserSchema:
    return await auth_service.register_user(user_data)


@router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginUserSchema)
async def auth_user(user_data: AuthUserSchema, auth_service: AuthService = Depends()) -> LoginUserSchema:
    return await auth_service.login_user(user_data)
