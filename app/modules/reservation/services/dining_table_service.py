
from datetime import timedelta, datetime, timezone
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.reservation.models.dining_table_model import DiningTable
from app.modules.reservation.repositories.dining_table_repository import DiningTableRepository
from app.modules.reservation.repositories.reservation_repotiory import ReservationRepository


class DiningTableService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = DiningTableRepository(db)
        self.reservation_repo = ReservationRepository(db)
    async def get_all(self):
        try:
            tables = await self.repository.get_all()
            return tables
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving attribute_values"
            )

    async def create(self, data: dict):
        # try:
            dining_table = await self.repository.create(DiningTable(**data))
            await self.db.commit()
            await self.db.refresh(dining_table)
            return dining_table
        # except Exception as e:
        #     raise HTTPException(
        #         status_code=500,
        #         detail=f"Internal server error while creating pizza: {str(e)}"
        #     )

    async def update(self, dining_table_id: int, data: dict):
        try:
            dining_table = await self.repository.update(dining_table_id, data)
            if not dining_table:
                raise HTTPException(
                    status_code=404,
                    detail=f"Option not found"
                )
            return dining_table
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while updating pizza: {str(e)}"
            )




    async def admin_get_all_tables(self):
        now = datetime.now(timezone.utc)
        tables= await self.repository.get_all()
        table_status = {}
        reservation = await self.reservation_repo.filter_reservations({"status": ["confirmed", "checked_in"]})
        for r in reservation:
            for t in r.tables:
                if r.start_time <= now <= r.end_time:
                    table_status[t.id] = "occupied"
                elif r.start_time - timedelta(minutes=60) <= now < r.start_time:
                    if t.id not in table_status:
                        table_status[t.id] = "preparing"
        result = [
            {
                "id": t.id,
                "name": t.name,
                "capacity": t.capacity,
                "status": table_status.get(t.id, "available")
            }
            for t in tables
        ]
        return result





