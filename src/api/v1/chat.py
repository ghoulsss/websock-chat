from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.services.auth import AuthService
from src.db.models.users import User

router = APIRouter(prefix="/chat", tags=["Chat"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse, summary="Chat Page")
async def get_chat_page(
    request: Request, auth_service: AuthService = Depends()
):
    user_data = auth_service.get_current_user()
    return templates.TemplateResponse(
        "chat.html", {"request": request, "user": user_data}
    )
