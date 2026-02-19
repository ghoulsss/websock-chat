from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from src.dependencies.auth import get_current_user
from src.db.models.users import User

router = APIRouter(prefix="/chat", tags=["Chat"])
templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse, summary="Chat Page")
async def get_chat_page(request: Request, user_data: User = Depends(get_current_user)):
    # users_all = await UsersDAO.find_all()
    return templates.TemplateResponse(
        "chat.html", {"request": request, "user": user_data, "users_all": "asd"}
    )
