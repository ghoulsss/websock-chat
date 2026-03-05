from fastapi import APIRouter, WebSocket, Depends
from services.chat import ChatService


router = APIRouter(prefix="", tags=["Websocket"])


@router.websocket("/ws/chat")
async def chat_websocket(
    websocket: WebSocket,
    chat_service: ChatService = Depends(),
):
    return await chat_service.chat_websocket(websocket)


# @router.websocket("/ws/chat")
# async def chat_websocket(
#     websocket: WebSocket,
#     session: AsyncSession = Depends(get_session),
#     auth_service: AuthService = Depends(),
#     messages_repo: MessagesRepository = Depends(),
# ):
#     user: User | None = None

#     try:
#         user = await auth_service.get_current_user_ws(websocket, session)

#         if not user:
#             await websocket.close(code=1008)
#             return

#         await manager.connect(websocket)
#         logger.info(f"User {user.name} (ID: {user.id}) connected to chat")

#         messages = await messages_repo.get_last_messages()

#         for msg in messages:
#             name = msg.user.name if msg.user else f"User {msg.user_id}"

#             await websocket.send_json(
#                 {
#                     "id": msg.id,
#                     "user_id": msg.user_id,
#                     "name": name,
#                     "content": msg.content,
#                     "created_at": msg.created_at,
#                 }
#             )

#         while True:
#             data = await websocket.receive_json()
#             content = data.get("content", "").strip()

#             if not content:
#                 continue

#             new_message = await messages_repo.create_message(user_id=user.id, content=content)

#             message_data = {
#                 "id": new_message.id,
#                 "user_id": user.id,
#                 "name": user.name,
#                 "content": new_message.content,
#                 "created_at": new_message.created_at.isoformat(),
#             }

#             await manager.broadcast(message_data)
#             # logger.info(f"Message from {user.name} broadcasted: {content[:30]}...")

#     except WebSocketDisconnect:
#         if user:
#             logger.info(f"User {user.name} disconnected from chat")

#         manager.disconnect(websocket)

#     except Exception as e:
#         logger.error(f"WebSocket error: {e}")

#         if user:
#             logger.exception(f"Error for user {user.name}")

#         manager.disconnect(websocket)

#     finally:
#         await session.close()
