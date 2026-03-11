from pydantic import EmailStr, Field
from schemas.base import BaseSchema


class CreateUserSchema(BaseSchema):
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


class AuthUserSchema(BaseSchema):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ..., min_length=5, max_length=30, description="Пароль, от 5 до 30 знаков"
    )

class CreateUserRepositorySchema(BaseSchema):
    email: EmailStr
    hashed_password: str
    name: str


class BaseUserSchema(BaseSchema):
    id: int
    name: str
    email: EmailStr


class GetUserSchema(BaseUserSchema): ...


class UpdateUserSchema(BaseSchema):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class GetUserEmailSchema(BaseSchema):
    id: int
    email: EmailStr
    hashed_password: str
