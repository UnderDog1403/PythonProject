from typing import List, Optional, Any, Dict, Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, asc, desc

from ..models.user_model import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_user_by_id(self, id) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.id == id)
        )
        return result.scalar_one_or_none()


    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()


    async def count_users(self) -> int:
        result = await self.db.execute(
            select(func.count(User.id))
        )
        return result.scalar_one()


    async def get_users_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "id",
        descending: bool = False,
    ) -> Tuple[List[User], int, int]:

        offset_value = max(page - 1, 0) * limit
        order_col = getattr(User, order_by, User.id)
        order_fn = desc if descending else asc

        # total count
        total_result = await self.db.execute(
            select(func.count(User.id))
        )
        total = total_result.scalar_one()

        # items
        items_result = await self.db.execute(
            select(User)
            .order_by(order_fn(order_col))
            .offset(offset_value)
            .limit(limit)
        )
        items = items_result.scalars().all()

        total_pages = (total + limit - 1) // limit if limit > 0 else 0

        return items, total, total_pages


    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()   # để có user.id
        return user


    async def update_user(
        self,
        user_id: str,
        data: Dict[str, Any],
    ) -> Optional[User]:

        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        for key, value in data.items():
            if key != "id" and hasattr(user, key):
                setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user


    async def update_active_status(
        self,
        user_id: str,
        is_active: bool,
    ) -> Optional[User]:

        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        user.is_active = is_active
        await self.db.commit()
        await self.db.refresh(user)

        return user
