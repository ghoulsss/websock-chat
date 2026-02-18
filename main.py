from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.v1.users import router as users_router
from src.api.v1.chat import router as chat_router
from src.api.v1.home import router as home_router
from src.api.v1.socket import router as socket_router
from src.api.v1.messages import router as messages_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(chat_router)
app.include_router(home_router)
app.include_router(socket_router)
app.include_router(messages_router)
