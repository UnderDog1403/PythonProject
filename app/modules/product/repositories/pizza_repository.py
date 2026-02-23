from typing import Any, Coroutine, Sequence

from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models.pizza_model import Pizza


class PizzaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_pizzas_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "id",
        descending: bool = False
    ) -> tuple[Sequence[Pizza], Any | None, int | Any]:
        offset_value = max(page - 1, 0) * limit
        order_col = getattr(Pizza, order_by, Pizza.id)
        order_fn = desc if descending else asc

        total_stmt = select(func.count()).select_from(Pizza)
        total = await self.db.scalar(total_stmt)

        stmt = (
            select(Pizza)
            .where(Pizza.is_actived.is_(True))
            .order_by(order_fn(order_col))
            .offset(offset_value)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        items = result.scalars().all()

        total_pages = (total + limit - 1) // limit if limit > 0 else 0

        return items, total, total_pages
    async def create(self, data: dict) -> Pizza:
        pizza = Pizza(**data)
        self.db.add(pizza)
        await self.db.commit()
        await self.db.refresh(pizza)
        return pizza
    async def get_pizza_by_id(self, pizza_id: int) -> Pizza | None:
        stmt = select(Pizza).where(Pizza.id == pizza_id)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    async def update(self, pizza_id: int, data: dict) -> Pizza | None:
        pizza = await self.get_pizza_by_id(pizza_id)
        if not pizza:
            return None
        for key, value in data.items():
            setattr(pizza, key, value)
        self.db.add(pizza)
        await self.db.commit()
        await self.db.refresh(pizza)
        return pizza
    async def delete(self, pizza_id: int) -> bool:
        pizza = await self.get_pizza_by_id(pizza_id)
        if not pizza:
            return False
        await self.db.delete(pizza)
        await self.db.commit()
        return True
