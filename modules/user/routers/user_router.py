from fastapi import APIRouter, Depends, HTTPException, status

from core.dependencies import db_dependency
from modules.user.schemas.user_schema import UserListResponseSchema
from modules.user.services.user_service import UserService

UserRouter= APIRouter(
    prefix="/users",
    tags=["Users"]
)
@UserRouter.get("/",status_code=status.HTTP_200_OK,response_model=UserListResponseSchema)
def get_users(
    db: db_dependency,
    page: int=1,
    limit: int=10
):
    user_service = UserService(db)
    users, total, total_page = user_service.get_users_paginated(page, limit)
    return UserListResponseSchema(
        users=users,
        total=total,
        total_pages=total_page,
        page =page,
        limit=limit
    )
@UserRouter.get("/{user_id}",status_code=status.HTTP_200_OK)
def get_user_by_id(
    user_id: str,
    db: db_dependency
):
    user_service = UserService(db)
    user = user_service.user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
