from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.reservation.models import DiningTable
from app.modules.reservation.models.reservation_model import Reservation
from app.modules.reservation.repositories.dining_table_repository import DiningTableRepository
from app.modules.reservation.repositories.reservation_repotiory import ReservationRepository


class ReservationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = ReservationRepository(db)
        self.table_repo = DiningTableRepository(db)
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
        try:
            start_time = data.get("start_time")
            end_time = start_time+ timedelta(hours=1)
            async with self.db.begin():
                result = await self.db.execute(
                    select(DiningTable)
                    .with_for_update()
                )
                locked_tables = result.scalars().all()
                available_tables = await self.repository.get_available_tables(
                    data["start_time"], end_time
                )
                total_seats = sum(table.capacity for table in available_tables)
                if total_seats < data["guest_count"]:
                    raise HTTPException(
                        status_code=400,
                        detail="Not enough available tables for the requested time slot"
                    )
                reservation = await self.repository.create(Reservation(**data, end_time=end_time))
                await self.db.commit()
                await self.db.refresh(reservation)
                return reservation
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating pizza: {str(e)}"
            )

    async def user_get_reservations(self, user_id: str):
        try:
            reservations = await self.repository.get_by_user_id(user_id)
            return reservations
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while retrieving reservations: {str(e)}"
            )
    async def admin_filter_reservations(self, data: dict):
        try:
            reservations = await self.repository.filter_reservations(data)
            return reservations
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while filtering reservations: {str(e)}"
            )
    async def admin_get_available_tables_for_reservation(self, reservation_id: int):
        # try:
            reservation = await self.repository.get_by_id(reservation_id)
            if not reservation:
                raise HTTPException(
                    status_code=404,
                    detail="Reservation not found"
                )
            available_tables = await self.repository.get_available_tables(
                reservation.start_time, reservation.end_time
            )
            return available_tables
        # except Exception as e:
        #     raise HTTPException(
        #         status_code=500,
        #         detail=f"Internal server error while retrieving available tables: {str(e)}"
        #     )
    async def admin_confirm_reservation(self, reservation_id: int, table_ids: list[int]):
        reservation = await self.repository.get_by_id(reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )
        available_tables = await self.repository.get_available_tables(
            reservation.start_time, reservation.end_time
        )
        available_table_ids = {table.id for table in available_tables}
        if not set(table_ids).issubset(available_table_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more selected tables are not available for the reservation time slot"
            )
        tables = await self.table_repo.get_by_ids(table_ids)
        total_seats = sum(table.capacity for table in tables)
        if total_seats < reservation.guest_count:
            raise HTTPException(
                status_code=400,
                detail="Selected tables do not have enough seats for the guest count"
            )
        reservation.tables = tables
        reservation.status = "confirmed"
        updated_reservation = await self.repository.update(reservation_id, reservation.__dict__)
        return updated_reservation

    async def admin_create_reservation(self, data: dict):
        try:
            start_time = data.get("start_time")
            end_time = start_time + timedelta(hours=1)
            available_tables = await self.repository.get_available_tables(
                data["start_time"], end_time
            )
            total_seats = sum(table.capacity for table in available_tables)
            if total_seats < data["guest_count"]:
                raise HTTPException(
                    status_code=400,
                    detail="Not enough available tables for the requested time slot"
                )
            reservation = await self.repository.create(Reservation(**data, end_time=end_time))
            await self.db.commit()
            await self.db.refresh(reservation)
            return reservation
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating pizza: {str(e)}"
            )

    async def admin_update_reservation(self, reservation_id: int, data: dict):
        try:
            reservation = await self.repository.get_by_id(reservation_id)
            if not reservation:
                raise HTTPException(
                    status_code=404,
                    detail="Reservation not found"
                )
            for key, value in data.items():
                setattr(reservation, key, value)
            updated_reservation = await self.repository.update(reservation_id, reservation.__dict__)
            return updated_reservation
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while updating reservation: {str(e)}"
            )


