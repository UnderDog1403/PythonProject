# modules/product/repositories/category_repository.py

from typing import List, Optional, Any, Dict, Tuple, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from app.modules.product.models.category_model import Category

class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all(self) -> Sequence[Category]:
        stmt = select(Category).where(Category.is_actived.is_(True))
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def admin_get_all(self) -> Sequence[Category]:
        stmt = select(Category)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False
    # ) -> Tuple[List[Category], int, int]:
    #
    #     offset_value = max(page - 1, 0) * limit
    #     order_col = getattr(Category, order_by, Category.id)
    #     order_fn = desc if descending else asc
    #
    #     # total count
    #     total_stmt = select(func.count()).select_from(Category)
    #     total = await self.db.scalar(total_stmt)
    #
    #     # items
    #     stmt = (
    #         select(Category)
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

    async def get_category_by_id(self, category_id: int) -> Optional[Category]:
        stmt = select(Category).where(Category.id == category_id)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()

    async def create_category(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Category:
        category = Category(name=name, description=description)
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update_category(
        self,
        category_id: int,
        data: Dict[str, Any]
    ) -> Optional[Category]:

        category = await self.get_category_by_id(category_id)
        if not category:
            return None

        for key, value in data.items():
            if key == "id":
                continue
            if hasattr(category, key):
                setattr(category, key, value)

        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete_category(self, category_id: int) -> bool:
        category = await self.get_category_by_id(category_id)
        if not category:
            return False

        await self.db.delete(category)
        await self.db.commit()
        return True
