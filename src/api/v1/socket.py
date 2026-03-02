from fastapi import APIRouter, WebSocket, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette.websockets import WebSocketDisconnect

from src.db.models import User, Message

from src.db.session import get_session
from src.dependencies.current_user import get_current_user_ws
from src.websocket.manager import manager
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["Websocket"])


@router.websocket("/ws/chat")
async def chat_websocket(
    websocket: WebSocket,
    session: AsyncSession = Depends(get_session),
):
    user = None

    try:
        user: User = await get_current_user_ws(websocket, session)

        if not user:
            await websocket.close(code=1008)
            return

        await manager.connect(websocket)
        logger.info(f"User {user.name} (ID: {user.id}) connected to chat")

        result = await session.execute(
            select(Message)
            .options(selectinload(Message.user))
            .order_by(Message.created_at.desc())
            .limit(50)
        )
        messages = result.scalars().all()
        messages.reverse()

        for msg in messages:
            name = msg.user.name if msg.user else f"User {msg.user_id}"

            await websocket.send_json({
                "id": msg.id,
                "user_id": msg.user_id,
                "name": name,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
            })

        while True:
            data = await websocket.receive_json()
            content = data.get("content", "").strip()

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
            logger.info(f"Message from {user.name} broadcasted: {content[:30]}...")

    except WebSocketDisconnect:
        if user:
            logger.info(f"User {user.name} disconnected from chat")

        manager.disconnect(websocket)

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

        if user:
            logger.exception(f"Error for user {user.name}")

        manager.disconnect(websocket)


    finally:
        await session.close()