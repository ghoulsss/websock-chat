from fastapi import Depends, WebSocket, status
from jose import jwt, JWTError
from core.config import settings
from db.repositories.user import UserRepository
from exceptions.auth import (
    IncorrectEmailOrPasswordException,
)
from schemas.auth import LoginUserSchema, RegisterUserSchema
from schemas.user import AuthUserSchema, CreateUserSchema, GetUserSchema
from services.user import UserService
from utils.auth import create_access_token, verify_password


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        user_service: UserService = Depends(),
    ) -> None:
        self._user_repository = user_repository
        self._user_service = user_service

    async def register_user(self, user_data: CreateUserSchema) -> RegisterUserSchema:
        user = await self._user_service.create_user(user_data=user_data)

        access_token = create_access_token(data={"sub": str(user.id)})

        return RegisterUserSchema.model_validate(
            {"access_token": access_token, "user": user}
        )

    async def login_user(self, auth_data: AuthUserSchema) -> LoginUserSchema:
        user = await self._user_repository.get_user_by_email(auth_data.email)
        if not user or not verify_password(
            plain_password=auth_data.password, hashed_password=user.hashed_password
        ):
            raise IncorrectEmailOrPasswordException

        access_token = create_access_token(data={"sub": str(user.id)})

        return LoginUserSchema.model_validate(
            {"access_token": access_token, "user": user}
        )

    async def get_current_user_ws(
        self,
        websocket: WebSocket,
    ) -> GetUserSchema | None:
        token = websocket.query_params.get("access_token")

        if not token:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        try:
            payload = jwt.decode(
                token, settings().SECRET_KEY, algorithms=[settings().ALGORITHM]
            )
            user_id = payload.get("sub")

            if user_id is None:
                await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
                return None

        except JWTError:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        user = await self._user_service.get_user_by_id(user_id=int(user_id))

        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        return user
