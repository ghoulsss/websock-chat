from typing import Sequence
from fastapi import HTTPException, Depends
from pydantic import EmailStr

from db.repositories.user import UserRepository
from schemas.user import CreateUserSchema, GetUserSchema, UpdateUserSchema
from utils.auth import get_password_hash


class UserService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
    ) -> None:
        self.user_repository = user_repository

    async def create_user(self, user_data: CreateUserSchema) -> GetUserSchema:
        hashed_password = get_password_hash(user_data.password)
        user = await self.user_repository.create_user(user_data, hashed_password)
        return user

    async def get_user_by_id(self, user_id: int) -> GetUserSchema:
        user = await self.user_repository.get_user_by_id(user_id=user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    async def get_user_by_email(self, email: EmailStr) -> GetUserSchema:
        user = await self.user_repository.get_user_by_email(email)

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return GetUserSchema.model_validate(user)

    async def get_all_users(self) -> Sequence[GetUserSchema]:
        return await self.user_repository.get_all_users()

    async def update_user(self, user_id: int, update_data: UpdateUserSchema) -> None:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        kwargs = update_data.model_dump(exclude_unset=True)

        if update_data.password and "password" in kwargs.keys():
            password = kwargs.pop("password")
            kwargs["hashed_password"] = get_password_hash(password)

        await self.user_repository.update_user(user_id=user_id, **kwargs)

    async def delete_user_by_id(self, user_id: int) -> None:
        await self.user_repository.delete_user_by_id(user_id=user_id)
