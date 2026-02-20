from fastapi import Request
from src.exceptions.auth import (
    TokenNoFoundException,
)


def get_token(request: Request):
    token = request.cookies.get("users_access_token")
    if not token:
        raise TokenNoFoundException
    return token
