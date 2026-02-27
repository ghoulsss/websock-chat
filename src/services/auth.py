from datetime import datetime, timezone

from fastapi import HTTPException, status, Depends
from jose import jwt, JWTError

# from src.dependencies.auth import get_token
from src.core.config import get_auth_data
from src.exceptions.auth import (
    TokenExpiredException,
    NoUserIdException,
    NoJwtException,
)
from src.exceptions.auth import IncorrectEmailOrPasswordException
from src.db.repositories.user import UserRepository
from src.exceptions.auth import UserAlreadyExistsException
from src.schemas.user import CreateUserSchema, AuthUserSchema, BaseUserSchema
from src.utils.auth import create_access_token, get_password_hash
from src.utils.auth import verify_password


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self._user_repository = user_repository

    async def register_user(self, user_data: CreateUserSchema):
        if user_data.password != user_data.password_check:
            raise ValueError("Passwords do not match")

        existing_user = await self._user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException(
                f"User with email {user_data.email} already exists"
            )

        hashed_password = get_password_hash(user_data.password)
        user = await self._user_repository.create_user(user_data, hashed_password)

        access_token = create_access_token({"sub": str(user.id)})
        return {"access_token": access_token, "user": user}

    async def login_user(self, auth_data: AuthUserSchema):
        user = await self._user_repository.get_user_by_email(auth_data.email)
        if not user or not verify_password(auth_data.password, user.hashed_password):
            return IncorrectEmailOrPasswordException

        access_token = create_access_token({"sub": str(user.id)})
        return {
            "access_token": access_token,
            "user": BaseUserSchema.model_validate(user),
        }
    #
    # async def get_current_user(self, token: str = Depends(get_token)):
    #     try:
    #         auth_data = get_auth_data()
    #         payload = jwt.decode(
    #             token, auth_data["secret_key"], algorithms=auth_data["algorithm"]
    #         )
    #     except JWTError:
    #         raise NoJwtException
    #
    #     expire: str = payload.get("exp")
    #     expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    #     if (not expire) or (expire_time < datetime.now(timezone.utc)):
    #         raise TokenExpiredException
    #
    #     user_id: str = payload.get("sub")
    #     if not user_id:
    #         raise NoUserIdException
    #
    #     user = await self._user_repository.get_user_by_id(int(user_id))
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
    #         )
    #     return user
