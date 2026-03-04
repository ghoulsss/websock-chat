from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.messages import Message
from db.models.mixins import UpdatedAtMixin, CreatedAtMixin, IDMixin
from db.models.base import BaseModel


class User(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)

    messages: Mapped["Message"] = relationship(back_populates="user")
