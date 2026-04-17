from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.order.models.order_item_model import OrderItem
from app.modules.order.models.order_model import Order


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_by_id(self, order_id: int):
        stmt = select(Order).options(
            selectinload(Order.items)
            .selectinload(OrderItem.options)
        ).where(Order.id == order_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    async def get_by_id_and_user_id(self, order_id: int, user_id: str):
        stmt = (select(Order)
                .options(
            selectinload(Order.items)
            .selectinload(OrderItem.options)
        )
                .where(Order.id == order_id, Order.user_id == user_id))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    async def create(self, order: Order):
        self.db.add(order)
        await self.db.flush()
        return order
    async def update(self, order_id: int, data: dict):
        stmt = select(Order).where(Order.id == order_id)
        result = await self.db.execute(stmt)
        order = result.scalar_one_or_none()
        if not order:
            return None
        for key, value in data.items():
            setattr(order, key, value)
        await self.db.commit()
        await self.db.refresh(order)
        return order
    async def get_all(self):
        stmt = select(Order)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def get_all_by_user_id(self, user_id: str):
        stmt = select(Order).where(Order.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()