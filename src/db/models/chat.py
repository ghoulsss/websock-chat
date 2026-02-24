from sqlalchemy import Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.mixins import IDMixin, CreatedAtMixin, UpdatedAtMixin
from src.db.models.base import BaseModel

class Chat(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "chats"

    name: Mapped[str | None]
    is_group: Mapped[bool] = mapped_column(Boolean, default=True)

class ChatMember(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "chat_members"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

class Message(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "messages"

    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
