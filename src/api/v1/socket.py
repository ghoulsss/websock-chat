import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.chat import Message
from src.db.session import get_session
from src.services.socket import manager
from src.services.auth import AuthService

router = APIRouter(prefix="/ws", tags=["WS"])


@router.websocket("/ws/chat/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, auth_repository: AuthService = Depends(), session: AsyncSession = Depends(get_session)):
    token = websocket.query_params.get("token")

    user = await auth_repository.get_current_user(token)

    await manager.connect(chat_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()

            message = Message(
                chat_id=chat_id,
                user_id=user.id,
                content=data["content"]
            )
            session.add(message)
            await session.commit()
            await session.refresh(message)

            await manager.broadcast(chat_id, {
                "user_id": user.id,
                "content": message.content,
                "created_at": str(message.created_at)
            })

    except WebSocketDisconnect:
        manager.disconnect(chat_id, websocket)
