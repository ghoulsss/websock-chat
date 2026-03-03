from fastapi import Depends

from exceptions.auth import IncorrectEmailOrPasswordException
from db.repositories.user import UserRepository
from exceptions.auth import UserAlreadyExistsException
from schemas.user import CreateUserSchema, AuthUserSchema, BaseUserSchema
from utils.auth import create_access_token, get_password_hash
from utils.auth import verify_password


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self._user_repository = user_repository

    async def register_user(self, user_data: CreateUserSchema):
        if user_data.password != user_data.password_check:
            raise ValueError("Passwords do not match")

        existing_user = await self._user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException

        hashed_password = get_password_hash(user_data.password)
        user = await self._user_repository.create_user(user_data, hashed_password)

        access_token = create_access_token({"sub": str(user.id)})
        return {"access_token": access_token, "user": user}

    async def login_user(self, auth_data: AuthUserSchema):
        user = await self._user_repository.get_user_by_email(auth_data.email)
        if not user or not verify_password(auth_data.password, user.hashed_password):
            return IncorrectEmailOrPasswordException

        access_token = create_access_token({"sub": str(user.id)})
        return {
            "access_token": access_token,
            "user": BaseUserSchema.model_validate(user),
        }
