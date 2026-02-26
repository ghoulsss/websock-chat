from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(prefix="/chat", tags=["Chat"])
templates = Jinja2Templates(directory="src/templates")

# @router.get("/", response_class=HTMLResponse)
# async def chat_interface(request: Request):
#     return templates.TemplateResponse("chat.html", {"request": request})
