

# modules/attribute/repositories/attribute_repository.py

from typing import List, Optional, Any, Dict, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from sqlalchemy.orm import selectinload

from app.modules.product.models.attribute_model import Attribute

class AttributeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all(self) -> Sequence[Attribute]:
        stmt =  select(Attribute).where(Attribute.is_active.is_(True)).options(
                selectinload(Attribute.values)
            )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def admin_get_all(self) -> Sequence[Attribute]:
        stmt = select(Attribute)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> Tuple[List[Attribute], int, int]:
    #
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(Attribute, order_by, Attribute.id)
    #     order_fn = desc if descending else asc
    #
    #     # total count
    #     total_stmt = select(func.count()).select_from(Attribute)
    #     total = await self.db.scalar(total_stmt)
    #
    #     # items
    #     stmt = (
    #         select(Attribute)
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
    async def get_by_id(self, attribute_id: int) -> Optional[Attribute]:
        stmt = select(Attribute).where(Attribute.id == attribute_id)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    async def create(self, data: dict):
        attribute = Attribute(**data)
        self.db.add(attribute)
        await self.db.commit()
        await self.db.refresh(attribute)
        return attribute
    async def update(
        self,
        attribute_id: int,
        data: Dict[str, Any]
    ) -> Optional[Attribute]:

        attribute = await self.get_by_id(attribute_id)
        if not attribute:
            return None
        for key, value in data.items():
            setattr(attribute, key, value)
        await self.db.commit()
        await self.db.refresh(attribute)
        return attribute

    async def delete(self, attribute_id: int) -> bool:
        attribute = await self.get_by_id(attribute_id)
        if not attribute:
            return False

        await self.db.delete(attribute)
        await self.db.commit()
        return True
