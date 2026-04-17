from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.reservation.models.dining_table_model import DiningTable


class DiningTableRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, dining_table_id: int):
        stmt = select(DiningTable).where(DiningTable.id == dining_table_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    async def get_by_ids(self, dining_table_ids: list[int]):
        stmt = select(DiningTable).where(DiningTable.id.in_(dining_table_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create(self, obj: DiningTable) -> DiningTable:
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, dining_table_id: int, data: dict):
        stmt = select(DiningTable).where(DiningTable.id == dining_table_id)
        result = await self.db.execute(stmt)
        dining_table = result.scalar_one_or_none()
        if not dining_table:
            return None
        for key, value in data.items():
            setattr(dining_table, key, value)
        await self.db.commit()
        await self.db.refresh(dining_table)
        return dining_table

    async def get_all(self):
        stmt = select(DiningTable)
        result = await self.db.execute(stmt)
        return result.scalars().all()
