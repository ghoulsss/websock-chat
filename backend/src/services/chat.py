from fastapi import Depends, WebSocket

from db.repositories.messages import MessagesRepository
from schemas.user import GetUserSchema
from services.auth import AuthService

from starlette.websockets import WebSocketDisconnect
from websocket.manager import manager
import logging

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(
        self,
        message_repository: MessagesRepository = Depends(),
        auth_service: AuthService = Depends(),
    ) -> None:
        self.message_repository = message_repository
        self.auth_service = auth_service

    async def chat_websocket(
        self,
        websocket: WebSocket,
    ):
        user = None

        try:
            user = await self.auth_service.get_current_user_ws(websocket)

            if not user:
                await websocket.close(code=1008)
                return

            await manager.connect(websocket)
            logger.info(f"User {user.name} (ID: {user.id}) connected to chat")

            messages = await self.message_repository.get_last_messages()

            for msg in messages:
                name = msg.user.name if msg.user else f"User {msg.user_id}"

                await websocket.send_json(
                    {
                        "id": msg.id,
                        "user_id": msg.user_id,
                        "name": name,
                        "content": msg.content,
                        "created_at": msg.created_at.isoformat(),
                    }
                )

            while True:
                data = await websocket.receive_json()
                content = data.get("content", "").strip()

                if not content:
                    continue

                new_message = await self.message_repository.create_message(
                    user_id=user.id, content=content
                )

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

    ########################################################################################
    # ########################################################################################
    async def get_recent_messages(self) -> list[dict]:
        messages = await self.message_repository.get_last_messages()

        result = []
        for msg in messages:
            name = msg.user.name if msg.user else f"User {msg.user_id}"
            result.append(
                {
                    "id": msg.id,
                    "user_id": msg.user_id,
                    "name": name,
                    "content": msg.content,
                    "created_at": msg.created_at,
                }
            )
        return result

    async def process_message(self, user: GetUserSchema, content: str) -> dict:
        new_message = await self.message_repository.create_message(user.id, content)

        return {
            "id": new_message.id,
            "user_id": user.id,
            "name": user.name,
            "content": new_message.content,
            "created_at": new_message.created_at,
        }
