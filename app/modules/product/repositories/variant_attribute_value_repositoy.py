

# modules/variant_attribute_value/repositories/variant_attribute_value_repository.py

from typing import List, Optional, Any, Dict, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from app.modules.product.models.variant_attribute_value_model import VariantAttributeValue

class VariantAttributeValueRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all(self) -> Sequence[VariantAttributeValue]:
        stmt = select(VariantAttributeValue)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> Tuple[List[VariantAttributeValue], int, int]:
    #
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(VariantAttributeValue, order_by, VariantAttributeValue.id)
    #     order_fn = desc if descending else asc
    #
    #     # total count
    #     total_stmt = select(func.count()).select_from(VariantAttributeValue)
    #     total = await self.db.scalar(total_stmt)
    #
    #     # items
    #     stmt = (
    #         select(VariantAttributeValue)
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

    async def create(self, data: dict):
        variant_attribute_value = VariantAttributeValue(**data)
        self.db.add(variant_attribute_value)
        await self.db.commit()
        await self.db.refresh(variant_attribute_value)
        return variant_attribute_value
    async def delete(self, variant_id, attribute_value_id):
        stmt = select(VariantAttributeValue).where(
            VariantAttributeValue.variant_id == variant_id,
            VariantAttributeValue.attribute_value_id == attribute_value_id
        )
        result = await self.db.execute(stmt)
        variant_attribute_value = result.scalars().one_or_none()
        if not variant_attribute_value:
            return False
        await self.db.delete(variant_attribute_value)
        await self.db.commit()
        return True


