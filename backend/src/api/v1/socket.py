from fastapi import APIRouter, WebSocket, Depends
from services.chat import ChatService


router = APIRouter(prefix="", tags=["Websocket"])


@router.websocket("/ws/chat")
async def chat_websocket(
    websocket: WebSocket,
    chat_service: ChatService = Depends(),
):
    return await chat_service.chat_websocket(websocket)
