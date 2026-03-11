from fastapi import Depends, WebSocket
from fastapi.encoders import jsonable_encoder

from db.repositories.messages import MessagesRepository
from schemas.message import SendMessageSchema
from services.auth import AuthService
from starlette.websockets import WebSocketDisconnect
from websocket.manager import manager



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
            user = await self.auth_service.get_current_user_ws(websocket=websocket)

            if not user:
                await websocket.close(code=1008)
                return

            await manager.connect(websocket)

            messages = await self.message_repository.get_last_messages()

            messages_data = jsonable_encoder([
                SendMessageSchema(
                    id=msg.id,
                    user_id=msg.user_id,
                    name=msg.user.name,
                    content=msg.content,
                    created_at=msg.created_at,
                ).model_dump()
            for msg in messages
            ])

            await websocket.send_json(messages_data)

            while True:
                data = await websocket.receive_json()
                content = data.get("content", "").strip()

                if not content:
                    continue

                new_message = await self.message_repository.create_message(
                    user_id=user.id, content=content
                )

                message_obj = SendMessageSchema(
                    id=new_message.id,
                    user_id=user.id,
                    name=user.name,
                    content=new_message.content,
                    created_at=new_message.created_at,
                )

                await manager.broadcast(jsonable_encoder(message_obj.model_dump()))

        except WebSocketDisconnect:
            manager.disconnect(websocket)
