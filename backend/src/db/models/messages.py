from typing import TYPE_CHECKING
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.mixins import IDMixin, CreatedAtMixin, UpdatedAtMixin
from db.models.base import BaseModel

from db.models.users import User


class Message(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "messages"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped[User] = relationship(back_populates="messages")
