from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect

# from db.session import get_session
# from src.services.auth import AuthService
# from src.db.models.users import User

router = APIRouter(prefix="/chat", tags=["Chat"])
templates = Jinja2Templates(directory="src/templates")


# @router.get("/", response_class=HTMLResponse, summary="Chat Page")
# async def get_chat_page(
#     request: Request, auth_service: AuthService = Depends()
# ):
#     user_data = auth_service.get_current_user()
#     return templates.TemplateResponse(
#         "chat.html", {"request": request, "user": user_data}
#     )
@router.get("/", response_class=HTMLResponse)
async def chat_interface(request):
    return templates.TemplateResponse("chat.html", {"request": request})

# Список подключенных клиентов
connected_clients = []

# Очередь сообщений
message_queue = []


# WebSocket для веб-интерфейса чата
@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    # Добавляем клиента в список подключенных
    connected_clients.append({"websocket": websocket, "username": username})
    # Приветственное сообщение для нового клиента
    welcome_message = f"Привет, {username}! Добро пожаловать в чат Otus!"
    await websocket.send_text(welcome_message)

    # Отправляем сообщения из очереди (если они есть)
    for message in message_queue:
        await websocket.send_text(message)

    try:
        while True:
            data = await websocket.receive_text()
            message = f"{username}: {data}"
            # Добавляем сообщение в очередь
            message_queue.append(message)
            # Отправляем сообщение всем подключенным клиентам
            for client in connected_clients:
                await client["websocket"].send_text(message)
    except WebSocketDisconnect:
        # Удаляем клиента из списка при отключении
        connected_clients.remove({"websocket": websocket, "username": username})


# Веб-страница для входа в чат
@router.get("/", response_class=HTMLResponse)
async def chat_interface(request):
    return templates.TemplateResponse("chat.html", {"request": request})