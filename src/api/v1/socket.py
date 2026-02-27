from fastapi import APIRouter, WebSocket, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models import User, Message

from src.db.session import get_session
from src.dependencies.current_user import get_current_user_ws
from src.websocket.manager import manager

router = APIRouter(prefix="", tags=["Websocket"])


@router.websocket("/ws/chat")
async def chat_websocket(
    websocket: WebSocket,
    session: AsyncSession = Depends(get_session),
):
    user: User = await get_current_user_ws(websocket, session)

    if not user:
        return

    await manager.connect(websocket)

    result = await session.execute(
        select(Message)
        .order_by(Message.created_at.desc())
        .limit(50)
    )
    messages = result.scalars().all()
    messages.reverse()

    for msg in messages:
        await websocket.send_json({
            "id": msg.id,
            "user_id": msg.user_id,
            "name": msg.user.name,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
        })

    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content")

            if not content:
                continue

            new_message = Message(
                user_id=user.id,
                content=content,
            )
            session.add(new_message)
            await session.commit()
            await session.refresh(new_message)

            message_data = {
                "id": new_message.id,
                "user_id": user.id,
                "name": user.name,
                "content": new_message.content,
                "created_at": new_message.created_at.isoformat(),
            }

            await manager.broadcast(message_data)

    except Exception:
        manager.disconnect(websocket)