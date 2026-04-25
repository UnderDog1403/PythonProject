

# modules/attribute_value/repositories/attribute_value_repository.py

from typing import List, Optional, Any, Dict, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from app.modules.product.models.attribute_value_model import AttributeValue

class AttributeValueRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all_by_attribute(self) -> Sequence[AttributeValue]:
        stmt = select(AttributeValue).where(AttributeValue.is_active.is_(True))
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def admin_get_all(self) -> Sequence[AttributeValue]:
        stmt = select(AttributeValue)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> Tuple[List[AttributeValue], int, int]:
    #
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(AttributeValue, order_by, AttributeValue.id)
    #     order_fn = desc if descending else asc
    #
    #     # total count
    #     total_stmt = select(func.count()).select_from(AttributeValue)
    #     total = await self.db.scalar(total_stmt)
    #
    #     # items
    #     stmt = (
    #         select(AttributeValue)
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
    async def get_by_id(self, attribute_value_id: int) -> Optional[AttributeValue]:
        stmt = select(AttributeValue).where(AttributeValue.id == attribute_value_id)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    async def get_by_ids(self, attribute_value_ids: List[int]) -> Sequence[AttributeValue]:
        stmt = select(AttributeValue).where(AttributeValue.id.in_(attribute_value_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def create(self, data: dict):
        attribute_value = AttributeValue(**data)
        self.db.add(attribute_value)
        await self.db.flush()
        return attribute_value
    async def update(
        self,
        attribute_value_id: int,
        data: Dict[str, Any]
    ) -> Optional[AttributeValue]:

        attribute_value = await self.get_by_id(attribute_value_id)
        if not attribute_value:
            return None
        for key, value in data.items():
            setattr(attribute_value, key, value)
        return attribute_value

    async def delete(self, attribute_value_id: int) -> bool:
        attribute_value = await self.get_by_id(attribute_value_id)
        if not attribute_value:
            return False

        await self.db.delete(attribute_value)
        await self.db.commit()
        return True
