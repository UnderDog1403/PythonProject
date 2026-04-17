

# modules/product_variant/repositories/product_variant_repository.py

from typing import List, Optional, Any, Dict, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from sqlalchemy.orm import selectinload

from app.modules.product.models.product_variant_model import ProductVariant

class ProductVariantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all_by_product_id(self,product_id: int) -> Sequence[ProductVariant]:
        stmt = select(ProductVariant).where(ProductVariant.product_id == product_id,ProductVariant.is_active.is_(True)).options(
                selectinload(ProductVariant.attribute_values)
            )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def admin_get_all(self) -> Sequence[ProductVariant]:
        stmt = select(ProductVariant)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> Tuple[List[ProductVariant], int, int]:
    #
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(ProductVariant, order_by, ProductVariant.id)
    #     order_fn = desc if descending else asc
    #
    #     # total count
    #     total_stmt = select(func.count()).select_from(ProductVariant)
    #     total = await self.db.scalar(total_stmt)
    #
    #     # items
    #     stmt = (
    #         select(ProductVariant)
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
    async def get_by_id(self, product_variant_id: int) -> Optional[ProductVariant]:
        stmt = select(ProductVariant).where(ProductVariant.id == product_variant_id)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    async def get_by_ids(self, product_variant_ids: List[int]) -> Sequence[ProductVariant]:
        stmt = select(ProductVariant).where(ProductVariant.id.in_(product_variant_ids)).options(
                selectinload(ProductVariant.product)
            )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: ProductVariant) -> ProductVariant:
        self.db.add(obj)
        await self.db.flush()
        return obj
    async def update(
        self,
        product_variant_id: int,
        data: Dict[str, Any]
    ) -> Optional[ProductVariant]:

        product_variant = await self.get_by_id(product_variant_id)
        if not product_variant:
            return None
        for key, value in data.items():
            setattr(product_variant, key, value)
        await self.db.commit()
        await self.db.refresh(product_variant)
        return product_variant

    async def delete(self, product_variant_id: int) -> bool:
        product_variant = await self.get_by_id(product_variant_id)
        if not product_variant:
            return False

        await self.db.delete(product_variant)
        await self.db.commit()
        return True
