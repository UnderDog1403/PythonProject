

# modules/option/repositories/option_repository.py

from typing import List, Optional, Any, Dict, Tuple, Sequence, Coroutine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from app.modules.product.models.option_model import Option

class OptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all(self) -> Sequence[Option]:
        stmt = select(Option).where(Option.is_active.is_(True))
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def admin_get_all(self) -> Sequence[Option]:
        stmt = select(Option)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> Tuple[List[Option], int, int]:
    #
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(Option, order_by, Option.id)
    #     order_fn = desc if descending else asc
    #
    #     # total count
    #     total_stmt = select(func.count()).select_from(Option)
    #     total = await self.db.scalar(total_stmt)
    #
    #     # items
    #     stmt = (
    #         select(Option)
    #         .order_by(order_fn(order_col))
    #         .offset(offset_value)
    #         .limit(limit)
    #     )
    #     result = await self.db.execute(stmt)
    #     items = result.scalars().all()
    #
    #     total_pages = (total + limit - 1) // limit if limit > 0 else 0
    #
    #     return items, total, total_pages
    # async def get_pizzas_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> tuple[Sequence[Pizza], Any | None, int | Any]:
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(Pizza, order_by, Pizza.id)
    #     order_fn = desc if descending else asc
    #
    #     total_stmt = select(func.count()).select_from(Pizza)
    #     total = await self.db.scalar(total_stmt)
    #
    #     stmt = (
    #         select(Pizza)
    #         .where(Pizza.is_actived.is_(True))
    #         .order_by(order_fn(order_col))
    #         .offset(offset_value)
    #         .limit(limit)
    #     )
    #     result = await self.db.execute(stmt)
    #     items = result.scalars().all()
    #
    #     total_pages = (total + limit - 1) // limit if limit > 0 else 0
    #
    #     return items, total, total_pages
    async def get_by_id(self, option_id: int) -> Optional[Option]:
        stmt = select(Option).where(Option.id == option_id)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    async def get_by_ids(self, option_ids: List[int]) -> Sequence[Option]:
        stmt = select(Option).where(Option.id.in_(option_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def create(self, data: dict):
        option = Option(**data)
        self.db.add(option)
        await self.db.commit()
        await self.db.refresh(option)
        return option
    async def update(
        self,
        option_id: int,
        data: Dict[str, Any]
    ) -> Optional[Option]:

        option = await self.get_by_id(option_id)
        if not option:
            return None
        for key, value in data.items():
            setattr(option, key, value)
        await self.db.commit()
        await self.db.refresh(option)
        return option

    async def delete(self, option_id: int) -> bool:
        option = await self.get_by_id(option_id)
        if not option:
            return False

        await self.db.delete(option)
        await self.db.commit()
        return True
