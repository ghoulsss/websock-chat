from typing import Sequence

from sqlalchemy import delete, insert, select, update

from db.repositories.base import BaseDatabaseRepository
from schemas.user import (
    CreateUserSchema,
    GetUserEmailSchema,
    GetUserSchema,
    UpdateUserSchema,
)
from db.models import User


class UserRepository(BaseDatabaseRepository):
    async def create_user(
        self, user_data: CreateUserSchema, hashed_password: str
    ) -> GetUserSchema:
        user_dict = user_data.model_dump(exclude={"password", "password_check"})
        user_dict["hashed_password"] = hashed_password

        query = insert(User).values(user_dict).returning(User)
        result = await self._session.execute(query)
        new_user = result.scalar_one()

        return GetUserSchema.model_validate(new_user)

    async def get_user_by_id(self, user_id: int) -> GetUserSchema | None:
        query = select(User).filter(User.id == user_id)

        result = await self._session.execute(query)
        user = result.scalars().first()

        return GetUserSchema.model_validate(user) if user else None

    async def get_user_by_email(self, email: str) -> GetUserEmailSchema | None:
        query = select(User).filter(User.email == email)

        result = await self._session.execute(query)
        user = result.scalars().first()

        return GetUserEmailSchema.model_validate(user) if user else None

    async def get_all_users(self) -> Sequence[GetUserSchema]:
        query = select(User)
        result = await self._session.execute(query)

        return [GetUserSchema.model_validate(user) for user in result.scalars().all()]

    async def update_user(self, user_id: int, update_data: UpdateUserSchema) -> None:
        query = (
            update(User)
            .where(User.id == user_id)
            .values(
                name=update_data.name,
                email=update_data.email,
                hashed_password=update_data.password,
            )
        )
        await self._session.execute(query)
        await self._session.flush()

    async def delete_user_by_id(self, user_id: int) -> None:
        query = delete(User).where(User.id == user_id)

        await self._session.execute(query)
        await self._session.flush()
