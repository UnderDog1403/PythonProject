from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.reservation.models import DiningTable
from app.modules.reservation.models.reservation_model import Reservation


class ReservationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, reservation_id: int):
        stmt = (select(Reservation)
                .options(selectinload(Reservation.tables))
                .where(Reservation.id == reservation_id))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: str):
        stmt = (select(Reservation)
                .options(selectinload(Reservation.tables))
                .where(Reservation.user_id == user_id))
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def filter_reservations(self, data: dict):
        stmt = select(Reservation)
        conditions = []
        status = data.get("status")
        if status:
            if isinstance(status, list):
                conditions.append(Reservation.status.in_(status))
            else:
                conditions.append(Reservation.status == status)
        customer_name = data.get("customer_name")
        if customer_name:
            conditions.append(
                Reservation.customer_name.ilike(f"%{customer_name}%")
            )
        customer_phone = data.get("customer_phone")
        if customer_phone:
            conditions.append(
                Reservation.customer_phone.ilike(f"%{customer_phone}%")
            )
        if conditions:
            stmt = stmt.options(
    selectinload(Reservation.tables)
).where(and_(*conditions))
        stmt = stmt.order_by(Reservation.start_time.asc())
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def create(self, obj: Reservation) -> Reservation:
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, reservation_id: int, data: dict):
        stmt = select(Reservation).where(Reservation.id == reservation_id)
        result = await self.db.execute(stmt)
        reservation = result.scalar_one_or_none()
        if not reservation:
            return None
        for key, value in data.items():
            setattr(reservation, key, value)
        await self.db.commit()
        await self.db.refresh(reservation)
        return reservation

    async def get_all(self):
        stmt = select(Reservation)
        result = await self.db.execute(stmt)
        return result.scalars().all()
    async def get_available_tables(self, start_time, end_time):
        tables = (await self.db.execute(
            select(DiningTable)
        )).scalars().all()
        reservations = (await self.db.execute(
            select(Reservation).where(
                Reservation.start_time < end_time,
                Reservation.end_time > start_time,
                Reservation.status == "confirmed"
            )
        )).scalars().all()
        occupied_table_ids = {
            table.id
            for r in reservations
            for table in r.tables
        }
        available_tables = [t for t in tables if t.id not in occupied_table_ids]
        return available_tables
