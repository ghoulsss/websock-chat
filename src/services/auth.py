from fastapi import Depends

from src.exceptions.auth import IncorrectEmailOrPasswordException
from src.db.repositories.user import UserRepository
from src.exceptions.auth import UserAlreadyExistsException
from src.schemas.user import SUserRegister, SUserAuth, SUser
from src.utils.auth import create_access_token, get_password_hash
from src.utils.auth import verify_password


class AuthService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self._user_repository = user_repository

    async def register_user(self, user_data: SUserRegister):
        if user_data.password != user_data.password_check:
            raise ValueError("Passwords do not match")

        existing_user = await self._user_repository.get_user_by_email(user_data.email)
        if existing_user:
            raise UserAlreadyExistsException(f"User with email {user_data.email} already exists")

        hashed_password = get_password_hash(user_data.password)
        user = await self._user_repository.create_user(user_data, hashed_password)

        access_token = create_access_token({"sub": str(user.id)})

        return {"access_token": access_token, "user": user}

    async def login_user(self, auth_data: SUserAuth):
        user = await self._authenticate_user(auth_data.email, auth_data.password)
        if not user:
            raise IncorrectEmailOrPasswordException

        access_token = create_access_token({"sub": str(user.id)})
        return {"access_token": access_token, "user": SUser.model_validate(user)}

    async def _authenticate_user(self, email: str, password: str):
        user = await self._user_repository.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user