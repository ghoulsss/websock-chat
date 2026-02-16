from fastapi import Depends
from sqlalchemy import select, and_, or_

from src.db.session import get_session
from src.dao.base import BaseDAO
from src.db.models.messages import Message


class MessagesDAO(BaseDAO):
    model = Message

    @classmethod
    async def get_messages_between_users(cls, user_id_1: int, user_id_2: int, session = Depends(get_session),):
        """
        Асинхронно находит и возвращает все сообщения между двумя пользователями.

        Аргументы:
            user_id_1: ID первого пользователя.
            user_id_2: ID второго пользователя.

        Возвращает:
            Список сообщений между двумя пользователями.
        """
        query = select(cls.model).filter(
            or_(
                and_(cls.model.sender_id == user_id_1, cls.model.recipient_id == user_id_2),
                and_(cls.model.sender_id == user_id_2, cls.model.recipient_id == user_id_1)
            )
        ).order_by(cls.model.id)
        result = await session.execute(query)
        return result.scalars().all()