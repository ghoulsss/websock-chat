from typing import Optional

from fastapi import WebSocket, status
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.config import settings
from db.models import User


async def get_current_user_ws(websocket: WebSocket, db: AsyncSession) -> Optional[User]:
    token = websocket.query_params.get("access_token")

    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    try:
        payload = jwt.decode(
            token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM]
        )

        user_id = payload.get("sub")  # int()
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return None

    return user
