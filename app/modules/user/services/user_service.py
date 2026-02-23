from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Tuple, Dict, Any

from ..models.user_model import User
from ..repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.db = db


    async def get_users_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "id",
        descending: bool = False,
    ) -> Tuple[List[User], int, int]:

        if page < 1 or limit < 1:
            raise HTTPException(
                status_code=400,
                detail="`page` and `limit` must be positive integers",
            )

        try:
            return await self.user_repo.get_users_paginated(
                page=page,
                limit=limit,
                order_by=order_by,
                descending=descending,
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving users",
            )


    async def get_user_by_id(self, user_id: str) -> User:
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user


    async def update_user(
        self,
        user_id: str,
        data: Dict[str, Any],
    ) -> User:

        if not isinstance(data, dict) or not data:
            raise HTTPException(
                status_code=400,
                detail="`data` must be a non-empty object with fields to update",
            )

        data = {k: v for k, v in data.items() if k != "id"}

        try:
            updated = await self.user_repo.update_user(user_id, data)
            if not updated:
                raise HTTPException(
                    status_code=404,
                    detail="User not found",
                )
            return updated
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while updating user",
            )


    async def update_active_status(
        self,
        user_id: str,
        is_active: bool,
    ) -> User:

        if not isinstance(is_active, bool):
            raise HTTPException(
                status_code=400,
                detail="`is_active` must be a boolean value",
            )

        try:
            updated = await self.user_repo.update_active_status(user_id, is_active)
            if not updated:
                raise HTTPException(
                    status_code=404,
                    detail="User not found",
                )
            return updated
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while updating user active status",
            )
