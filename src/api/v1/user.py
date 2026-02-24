from typing import Sequence
from fastapi import APIRouter, Depends, status

from src.schemas.user import UpdateUserSchema
from src.services.user import UserService
from src.schemas.user import BaseUserSchema, CreateUserSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_200_OK, response_model=BaseUserSchema)
async def create_user(
    user_data: CreateUserSchema, user_service: UserService = Depends()
) -> BaseUserSchema:
    return await user_service.create_user(user_data)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=BaseUserSchema)
async def get_user(
    user_id: int, user_service: UserService = Depends()
) -> BaseUserSchema:
    return await user_service.get_user_by_id(user_id)


@router.get("", status_code=status.HTTP_200_OK, response_model=Sequence[BaseUserSchema])
async def list_users(
    # lim: int = 10, добавить
    # offset: int = 0,
    user_service: UserService = Depends(),
) -> Sequence[BaseUserSchema]:
    return await user_service.list_users()


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int, update_data: UpdateUserSchema, service: UserService = Depends()
):
    return await service.update_user(
        user_id=user_id,
        update_data=update_data.model_dump(exclude_unset=True),
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, service: UserService = Depends()):
    await service.delete_user(user_id)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users(service: UserService = Depends()):
    await service.delete_all_users()
