from typing import Sequence
from fastapi import APIRouter, Depends, status

from schemas.user import GetUserSchema, UpdateUserSchema
from services.user import UserService
from schemas.user import CreateUserSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_user(
    user_data: CreateUserSchema, user_service: UserService = Depends()
):
    return await user_service.create_user(user_data=user_data)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=GetUserSchema)
async def get_user_by_id(
    user_id: int, user_service: UserService = Depends()
) -> GetUserSchema:
    return await user_service.get_user_by_id(user_id=user_id)


@router.get("", status_code=status.HTTP_200_OK, response_model=Sequence[GetUserSchema])
async def get_all_users(
    user_service: UserService = Depends(),
) -> Sequence[GetUserSchema]:
    return await user_service.get_all_users()


@router.patch("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def update_user_by_id(
    user_id: int, update_data: UpdateUserSchema, service: UserService = Depends()
) -> None:
    return await service.update_user_by_id(
        user_id=user_id,
        update_data=update_data,
    )


@router.delete(
    "/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None
)
async def delete_user_by_id(user_id: int, service: UserService = Depends()) -> None:
    await service.delete_user_by_id(user_id=user_id)
