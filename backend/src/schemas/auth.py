from pydantic import EmailStr, Field
from schemas.base import BaseSchema


class RegisterUserSchema(BaseSchema):
    access_token: str = Field(..., description="Токен")
    user: dict = Field(
        ..., description="Данные пользователя"
    )


class LoginUserSchema(RegisterUserSchema):
    ...
