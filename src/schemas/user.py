from pydantic import EmailStr, Field
from src.schemas.base import BaseSchema


class SUserRegister(BaseSchema):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ..., min_length=5, max_length=30, description="Пароль, от 5 до 30 знаков"
    )
    password_check: str = Field(
        ..., min_length=5, max_length=30, description="Пароль, от 5 до 30 знаков"
    )
    name: str = Field(
        ..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов"
    )


class SUserAuth(BaseSchema):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ..., min_length=5, max_length=30, description="Пароль, от 5 до 30 знаков"
    )

class SUser(BaseSchema):
    id: int
    name: str
    email: EmailStr