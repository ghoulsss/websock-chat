from datetime import datetime
from schemas.base import BaseSchema
from schemas.user import GetUserSchema


class BaseMessageSchema(BaseSchema):
    id: int
    user_id: int
    content: str
    created_at: datetime


class GetMessageSchema(BaseMessageSchema):
    created_at: datetime

    user: GetUserSchema


class SendMessageSchema(BaseMessageSchema):
    name: str
