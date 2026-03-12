

# modules/option_value/repositories/option_value_repository.py

from typing import List, Optional, Any, Dict, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from app.modules.product.models.option_value_model import OptionValue

class OptionValueRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all(self) -> Sequence[OptionValue]:
        stmt = select(OptionValue).where(OptionValue.is_active.is_(True))
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def admin_get_all(self) -> Sequence[OptionValue]:
        stmt = select(OptionValue)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> Tuple[List[OptionValue], int, int]:
    #
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(OptionValue, order_by, OptionValue.id)
    #     order_fn = desc if descending else asc
    #
    #     # total count
    #     total_stmt = select(func.count()).select_from(OptionValue)
    #     total = await self.db.scalar(total_stmt)
    #
    #     # items
    #     stmt = (
    #         select(OptionValue)
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
    async def get_by_id(self, option_value_id: int) -> Optional[OptionValue]:
        stmt = select(OptionValue).where(OptionValue.id == option_value_id)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    async def create(self, data: dict):
        option_value = OptionValue(**data)
        self.db.add(option_value)
        await self.db.commit()
        await self.db.refresh(option_value)
        return option_value
    async def update(
        self,
        option_value_id: int,
        data: Dict[str, Any]
    ) -> Optional[OptionValue]:

        option_value = await self.get_by_id(option_value_id)
        if not option_value:
            return None
        for key, value in data.items():
            setattr(option_value, key, value)
        await self.db.commit()
        await self.db.refresh(option_value)
        return option_value

    async def delete(self, option_value_id: int) -> bool:
        option_value = await self.get_by_id(option_value_id)
        if not option_value:
            return False

        await self.db.delete(option_value)
        await self.db.commit()
        return True
