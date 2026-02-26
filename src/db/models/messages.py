from sqlalchemy import Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.mixins import IDMixin, CreatedAtMixin, UpdatedAtMixin
from src.db.models.base import BaseModel


class Message(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "messages"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        # nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship(back_populates="messages")
