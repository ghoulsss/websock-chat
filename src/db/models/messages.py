# from sqlalchemy import Integer, Text, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column
#
# from src.db.models.mixins import IDMixin, CreatedAtMixin, UpdatedAtMixin
# from src.db.models.base import BaseModel
#
#
# class Message(BaseModel, IDMixin, CreatedAtMixin, UpdatedAtMixin):
#     __tablename__ = "messages"
#
#     sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
#     recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
#     content: Mapped[str] = mapped_column(Text)
