from typing import Sequence

from sqlalchemy import Delete, select, update

from db.repositories.base import BaseDatabaseRepository
from schemas.user import CreateUserSchema, BaseUserSchema
from db.models import User


class UserRepository(BaseDatabaseRepository):
    async def create_user(
        self, user_data: CreateUserSchema, hashed_password: str
    ) -> BaseUserSchema:
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        self._session.add(new_user)
        await self._session.flush()

        return BaseUserSchema.model_validate(new_user)

    async def get_user_by_id(self, user_id: int) -> BaseUserSchema | None:
        user = await self._session.get(User, user_id)
        return BaseUserSchema.model_validate(user) if user else None

    async def get_user_by_email(self, email: str) -> User | None:
        query = select(User).where(User.email == email)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_all_users(self) -> Sequence[BaseUserSchema]:
        query = select(User)
        result = await self._session.execute(query)

        return [BaseUserSchema.model_validate(user) for user in result.scalars().all()]

    async def update_user(self, user_id: int, update_data: dict) -> None:
        await self._session.execute(
            update(User).where(User.id == user_id).values(**update_data)
        )
        await self._session.flush()

    async def delete_user(self, user_id: int) -> None:
        await self._session.execute(Delete(User).where(User.id == user_id))
        await self._session.flush()

    async def delete_all(self) -> None:
        await self._session.execute(Delete(User))
        await self._session.flush()
