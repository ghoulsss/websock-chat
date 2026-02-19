from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.mixins import UpdatedAtMixin, CreatedAtMixin, IDMixin
from src.db.models.base import BaseModel


class User(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
