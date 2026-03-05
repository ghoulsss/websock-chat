from fastapi import Depends, WebSocket, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from core.config import settings
from db.models import User
from db.repositories.user import UserRepository
from db.session import get_session
from exceptions.auth import (
    IncorrectEmailOrPasswordException,
    PasswordMismatchException,
    UserAlreadyExistsException,
)
from schemas.auth import LoginUserSchema, RegisterUserSchema
from schemas.user import AuthUserSchema, CreateUserSchema, GetUserSchema
from services.user import UserService
from utils.auth import create_access_token, get_password_hash, verify_password


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends(),
                 user_service: UserService = Depends()) -> None:
        self._user_repository = user_repository
        self._user_service = user_service

    async def register_user(self, user_data: CreateUserSchema) -> RegisterUserSchema:
        try:
            if user_data.password != user_data.password_check:
                raise ValueError("Passwords do not match")

            existing_user = await self._user_repository.get_user_by_email(
                email=user_data.email
            )
            print(existing_user)
            if existing_user:
                raise UserAlreadyExistsException

            hashed_password = get_password_hash(user_data.password)
            user = await self._user_repository.create_user(user_data, hashed_password=hashed_password)

            access_token = create_access_token({"sub": str(user.id)})

            return RegisterUserSchema.model_validate(
                {"access_token": access_token, "user": user}
            )

        except ValueError:
            raise PasswordMismatchException
        except Exception as e:
            # Логируем неожиданную ошибку и выбрасываем общее исключение
            print(f"Unexpected error during registration: {e}")
            # Здесь лучше выбросить другое исключение, например InternalServerError
            raise Exception("Registration failed due to internal error")

    async def login_user(self, auth_data: AuthUserSchema) -> LoginUserSchema:
        try:
            user = await self._user_repository.get_user_by_email(auth_data.email)
            if not user or not verify_password(
                auth_data.password, user.hashed_password
            ):
                raise IncorrectEmailOrPasswordException

            access_token = create_access_token({"sub": str(user.id)})

            return LoginUserSchema.model_validate(
                {"access_token": access_token, "user": user}
            )
        except Exception:
            raise Exception

    async def get_current_user_ws(
        self, websocket: WebSocket,
        # session: AsyncSession = Depends(get_session)
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
        except JWTError:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        user = await self._user_service.get_user_by_id(user_id=int(user_id))
        # result = await session.execute(select(User).filter(User.id == user_id))
        # user = result.scalar_one_or_none()

        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return None

        return user
