# src/dependencies/auth_ws.py

from jose import jwt
from fastapi import WebSocket, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_session
from src.core.config import get_auth_data
from src.db.repositories.user import UserRepository


async def get_current_user_ws(websocket: WebSocket, session: AsyncSession = Depends(get_session)):
    token = websocket.cookies.get("users_access_token")
    if not token:
        await websocket.close(code=1008)
        return None

    auth_data = get_auth_data()
    payload = jwt.decode(
        token,
        auth_data["secret_key"],
        algorithms=[auth_data["algorithm"]],
    )

    user_id = payload.get("sub")

    repo = UserRepository(session)
    user = await repo.get_user_by_id(int(user_id))
    return user