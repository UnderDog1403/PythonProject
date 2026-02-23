from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import db_dependency
from app.modules.user.schemas.user_schema import (
    UserListResponseSchema,
    UserUpdateSchema,
    UserResponseSchema,
    UserUpdateActiveSchema,
)
from app.modules.user.services.user_service import UserService


UserRouter = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@UserRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=UserListResponseSchema,
)
async def get_users(
    db: db_dependency,
    page: int = 1,
    limit: int = 10,
    order_by: str = "id",
    descending: bool = False,
):
    user_service = UserService(db)

    users, total, total_page = await user_service.get_users_paginated(
        page, limit, order_by, descending
    )

    return UserListResponseSchema(
        users=users,
        total=total,
        total_pages=total_page,
        page=page,
        limit=limit,
    )


@UserRouter.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
)
async def get_user_by_id(
    user_id: str,
    db: db_dependency,
):
    user_service = UserService(db)

    user = await user_service.user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@UserRouter.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
)
async def update_user(
    user_id: str,
    payload: UserUpdateSchema,
    db: db_dependency,
):
    user_service = UserService(db)

    updated_user = await user_service.update_user(
        user_id,
        payload.model_dump(exclude_unset=True),
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return updated_user


@UserRouter.put(
    "/{user_id}/activate",
    status_code=status.HTTP_200_OK,
    response_model=UserResponseSchema,
)
async def update_active_status(
    user_id: str,
    payload: UserUpdateActiveSchema,
    db: db_dependency,
):
    user_service = UserService(db)

    updated_user = await user_service.update_active_status(
        user_id,
        payload.is_active,
    )

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return updated_user
