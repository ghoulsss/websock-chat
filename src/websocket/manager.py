from typing import Dict, List

from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.usernames: dict = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            if websocket in self.usernames:
                del self.usernames[websocket]

    async def send_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except:
            self.disconnect(websocket)

    async def broadcast(self, message: str, sender: WebSocket = None):
        disconnected = []
        for connection in self.active_connections:
            if connection != sender:
                try:
                    await connection.send_text(message)
                except:
                    disconnected.append(connection)

        for conn in disconnected:
            self.disconnect(conn)


manager = ConnectionManager()
