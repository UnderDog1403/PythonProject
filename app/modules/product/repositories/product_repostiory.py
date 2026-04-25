

# modules/product/repositories/product_repository.py

from typing import List, Optional, Any, Dict, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from sqlalchemy.orm import selectinload

from app.modules.product.models.attribute_value_model import AttributeValue
from app.modules.product.models.option_model import Option
from app.modules.product.models.product_model import Product
from app.modules.product.models.product_variant_model import ProductVariant


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        stmt = (
            select(Product)
            .where(Product.is_active == True)
            .options(
                selectinload(Product.variants.and_(ProductVariant.is_active == True))
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def admin_get_all(self) -> Sequence[Product]:
        stmt = (select(Product)
                .options(selectinload(Product.variants))
                )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> Tuple[List[Product], int, int]:
    #
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(Product, order_by, Product.id)
    #     order_fn = desc if descending else asc
    #
    #     # total count
    #     total_stmt = select(func.count()).select_from(Product)
    #     total = await self.db.scalar(total_stmt)
    #
    #     # items
    #     stmt = (
    #         select(Product)
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
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        stmt = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                selectinload(Product.variants)
                .selectinload(ProductVariant.attribute_values)
                .selectinload(AttributeValue.attribute),
                selectinload(Product.options)
                .selectinload(Option.values)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    async def create(self, obj: Product) -> Product:
        self.db.add(obj)
        await self.db.flush()
        return obj
    async def update(
        self,
        product_id: int,
        data: Dict[str, Any]
    ) -> Optional[Product]:

        product = await self.get_by_id(product_id)
        if not product:
            return None
        for key, value in data.items():
            setattr(product, key, value)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product_id: int) -> bool:
        product = await self.get_by_id(product_id)
        if not product:
            return False

        await self.db.delete(product)
        await self.db.commit()
        return True
