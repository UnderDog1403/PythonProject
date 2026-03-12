from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.promotion.models.voucher_model import Voucher


class VoucherRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def get_all(self):
        stmt = select(Voucher)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def create(self, data: dict):
        voucher = Voucher(**data)
        self.db.add(voucher)
        await self.db.commit()
        await self.db.refresh(voucher)
        return voucher
    async def update(self, voucher_id: int, data: dict):
        stmt = select(Voucher).where(Voucher.id == voucher_id)
        result = await self.db.execute(stmt)
        voucher = result.scalar_one_or_none()
        if not voucher:
            return None
        for key, value in data.items():
            setattr(voucher, key, value)
        await self.db.commit()
        await self.db.refresh(voucher)
        return voucher
    async def delete(self, voucher_id: int) -> bool:
        stmt = select(Voucher).where(Voucher.id == voucher_id)
        result = await self.db.execute(stmt)
        voucher = result.scalar_one_or_none()
        if not voucher:
            return False
        await self.db.delete(voucher)
        await self.db.commit()
        return True
    async def get_by_id(self, voucher_id: int):
        stmt = select(Voucher).where(Voucher.id == voucher_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

