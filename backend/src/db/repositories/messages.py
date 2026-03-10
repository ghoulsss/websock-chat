from typing import Sequence
from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload

from db.models import Message
from db.repositories.base import BaseDatabaseRepository
from schemas.message import GetMessageSchema


class MessagesRepository(BaseDatabaseRepository):
    async def get_last_messages(self, limit: int = 50) -> Sequence[GetMessageSchema]:
        query = (
            select(Message)
            .options(selectinload(Message.user))
            .order_by(Message.created_at.asc())
            .limit(limit)
        )

        result = await self._session.execute(query)

        return [
            GetMessageSchema.model_validate(user) for user in result.scalars().all()
        ]

    async def create_message(self, user_id: int, content: str) -> GetMessageSchema:
        query = (
            insert(Message)
            .values(user_id=user_id, content=content)
            .returning(Message.id)
        )

        result = await self._session.execute(query)
        new_message_id = result.scalar_one()

        select_query = (
            select(Message)
            .options(selectinload(Message.user))
            .where(Message.id == new_message_id)
        )
        select_result = await self._session.execute(select_query)
        new_message = select_result.scalar_one()

        return GetMessageSchema.model_validate(new_message)
