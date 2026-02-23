from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.models.pizza_size_model import PizzaSize


class PizzaSizeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all(self):
        stmt = select(PizzaSize).where(PizzaSize.is_actived.is_(True))
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def get_by_id(self, pizza_size_id: int):
        stmt = select(PizzaSize).where(PizzaSize.id == pizza_size_id)
        result = await self.db.execute(stmt)
        return result.scalars().one_or_none()
    async def create(self, data: dict):
        pizza_size = PizzaSize(**data)
        self.db.add(pizza_size)
        await self.db.commit()
        await self.db.refresh(pizza_size)
        return pizza_size
    async def update(self, pizza_size_id: int, data: dict):
        pizza_size = await self.get_by_id(pizza_size_id)
        if not pizza_size:
            return None
        for key, value in data.items():
            setattr(pizza_size, key, value)
        self.db.add(pizza_size)
        await self.db.commit()
        await self.db.refresh(pizza_size)
        return pizza_size
    async def delete(self, pizza_size_id: int):
        pizza_size = await self.get_by_id(pizza_size_id)
        if not pizza_size:
            return False
        await self.db.delete(pizza_size)
        await self.db.commit()
        return True

