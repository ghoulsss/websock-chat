from typing import Sequence
from fastapi import Depends
from pydantic import EmailStr

from db.repositories.user import UserRepository
from exceptions.auth import (
    PasswordMismatchException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from schemas.user import (
    CreateUserSchema,
    GetUserSchema,
    UpdateUserSchema,
    CreateUserRepositorySchema,
)
from utils.auth import get_password_hash


class UserService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
    ) -> None:
        self._user_repository = user_repository

    async def create_user(self, user_data: CreateUserSchema) -> GetUserSchema:
        if user_data.password != user_data.password_check:
            raise PasswordMismatchException

        if await self._user_repository.get_user_by_email(email=user_data.email):
            raise UserAlreadyExistsException

        data = user_data.model_dump(exclude={"password", "password_check"})
        data["hashed_password"] = get_password_hash(password=user_data.password)

        user = await self._user_repository.create_user(
            data=CreateUserRepositorySchema.model_validate(data)
        )
        return user

    async def get_user_by_id(self, user_id: int) -> GetUserSchema:
        user = await self._user_repository.get_user_by_id(user_id=user_id)

        if not user:
            raise UserNotFoundException

        return user

    async def get_user_by_email(self, email: EmailStr) -> GetUserSchema:
        user = await self._user_repository.get_user_by_email(email)

        if not user:
            raise UserNotFoundException

        return GetUserSchema.model_validate(user)

    async def get_all_users(self) -> Sequence[GetUserSchema]:
        return await self._user_repository.get_all_users()

    async def update_user_by_id(
        self, user_id: int, update_data: UpdateUserSchema
    ) -> None:
        if not await self.get_user_by_id(user_id):
            raise UserNotFoundException

        kwargs = update_data.model_dump(exclude_unset=True)

        if update_data.password and "password" in kwargs.keys():
            password = kwargs.pop("password")
            kwargs["hashed_password"] = get_password_hash(password)

        await self._user_repository.update_user(user_id=user_id, **kwargs)

    async def delete_user_by_id(self, user_id: int) -> None:
        await self._user_repository.delete_user_by_id(user_id=user_id)
