from pydantic import Field
from schemas.base import BaseSchema
from schemas.user import GetUserEmailSchema, GetUserSchema

class BaseAuthUserSchema(BaseSchema):
    access_token: str = Field(..., description="Токен")

class RegisterUserSchema(BaseAuthUserSchema):
    user: GetUserSchema


class LoginUserSchema(BaseAuthUserSchema):
    user: GetUserEmailSchema
