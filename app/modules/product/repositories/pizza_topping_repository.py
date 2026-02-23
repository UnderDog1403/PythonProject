from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models.pizza_topping_model import PizzaTopping


class PizzaToppingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all(self):
        stmt = select(PizzaTopping).where(PizzaTopping.is_actived.is_(True))
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def get_by_id(self, pizza_topping_id: int):
        stmt = select(PizzaTopping).where(PizzaTopping.id == pizza_topping_id)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    async def create(self,data: dict):
        pizza_topping = PizzaTopping(**data)
        self.db.add(pizza_topping)
        await self.db.commit()
        await self.db.refresh(pizza_topping)
        return pizza_topping
    async def update(self, pizza_topping_id: int, data: dict):
        pizza_topping = await self.get_by_id(pizza_topping_id)
        if not pizza_topping:
            return None
        for key, value in data.items():
            setattr(pizza_topping, key, value)
        await self.db.commit()
        await self.db.refresh(pizza_topping)
        return pizza_topping
    async def delete(self, pizza_topping_id: int):
        pizza_topping = await self.get_by_id(pizza_topping_id)
        if not pizza_topping:
            return False
        await self.db.delete(pizza_topping)
        await self.db.commit()
        return True
