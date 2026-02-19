from typing import Sequence

from pydantic import EmailStr

from db.repositories.user import UserRepository
from schemas.user import SUserRegister, SUser
from utils.auth import get_password_hash, authenticate_user, create_access_token


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: SUserRegister) -> SUser:
        hashed_password = get_password_hash(user_data.password)
        user = await self.repository.create_user(user_data, hashed_password)
        return user

    async def get_user_by_id(self, user_id: int) -> SUser | None:
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_email(self, user_id: int) -> SUser | None:
        return await self.repository.get_user_by_id(user_id)

    async def get_all_users(self) -> Sequence[SUser]:
        return await self.repository.get_all_users()

    async def list_users(self) -> Sequence[SUser]:
        return await self.repository.get_all_users()

    async def update_user(self, user_id: int, update_data: dict) -> None:
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        await self.repository.update_user(user_id, update_data)

    async def delete_user(self, user_id: int) -> None:
        await self.repository.delete_user(user_id)

    async def delete_all_users(self) -> None:
        await self.repository.delete_all()
