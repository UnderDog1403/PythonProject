

# modules/product_option/repositories/product_option_repository.py

from typing import List, Optional, Any, Dict, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from app.modules.product.models.product_option_model import ProductOption

class ProductOptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all(self) -> Sequence[ProductOption]:
        stmt = select(ProductOption)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> Tuple[List[ProductOption], int, int]:
    #
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(ProductOption, order_by, ProductOption.id)
    #     order_fn = desc if descending else asc
    #
    #     # total count
    #     total_stmt = select(func.count()).select_from(ProductOption)
    #     total = await self.db.scalar(total_stmt)
    #
    #     # items
    #     stmt = (
    #         select(ProductOption)
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
        product_option = ProductOption(**data)
        self.db.add(product_option)
        await self.db.commit()
        await self.db.refresh(product_option)
        return product_option
    async def delete(self, product_id, option_id):
        stmt = select(ProductOption).where(
            ProductOption.product_id == product_id,
            ProductOption.option_id == option_id
        )
        result = await self.db.execute(stmt)
        product_option = result.scalars().one_or_none()
        if not product_option:
            return False
        await self.db.delete(product_option)
        await self.db.commit()
        return True


