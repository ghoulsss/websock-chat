from schemas.base import BaseSchema
from schemas.user import GetUserSchema


class GetMessageSchema(BaseSchema):
    id: int
    user_id: int
    content: str
    updated_at: str
    created_at: str

    user: GetUserSchema
