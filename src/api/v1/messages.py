from fastapi import Depends, APIRouter
from typing import List
from src.dao.chat import MessagesDAO
from src.schemas.messages import MessageRead, MessageCreate
from src.dependencies.auth import get_current_user
from src.db.models.users import User
from src.api.v1.socket import notify_user

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.get("/{user_id}", response_model=List[MessageRead])
async def get_messages(user_id: int, current_user: User = Depends(get_current_user)):
    return (
        await MessagesDAO.get_messages_between_users(
            user_id_1=user_id, user_id_2=current_user.id
        )
        or []
    )


@router.post("", response_model=MessageCreate)
async def send_message(
    message: MessageCreate, current_user: User = Depends(get_current_user)
):
    await MessagesDAO.add(
        sender_id=current_user.id,
        content=message.content,
        recipient_id=message.recipient_id,
    )
    message_data = {
        "sender_id": current_user.id,
        "recipient_id": message.recipient_id,
        "content": message.content,
    }
    await notify_user(message.recipient_id, message_data)
    await notify_user(current_user.id, message_data)

    return {
        "recipient_id": message.recipient_id,
        "content": message.content,
        "status": "ok",
        "msg": "Message saved!",
    }
