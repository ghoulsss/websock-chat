from datetime import datetime
from schemas.base import BaseSchema


class MessageCreate(BaseSchema):
    content: str


class MessageOut(MessageCreate):
    id: int
    user_id: int
    username: str
    created_at: datetime
