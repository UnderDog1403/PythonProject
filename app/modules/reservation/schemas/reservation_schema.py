from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.modules.reservation.models.reservation_model import ReservationStatus


class ReservationResponse(BaseModel):
    id: int

    user_id: Optional[UUID]
    customer_name: str
    customer_phone: str
    source: str

    guest_count: int
    start_time: datetime
    end_time: datetime

    status: str
    note: Optional[str]

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class ReservationCreate(BaseModel):
    customer_name: str
    customer_phone: str
    guest_count: int
    start_time: datetime
    note: Optional[str] = None
class ReservationFilter(BaseModel):
    status: Optional[ReservationStatus] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
class AdminConfirmReservationRequest(BaseModel):
    table_ids: list[int]
class AdminReservationCreate(BaseModel):
    customer_name: str
    customer_phone: str
    guest_count: int
    start_time: datetime
    note: Optional[str] = None
    source: str = "pos"
    status: Optional[ReservationStatus] = "confirmed"
class AdminReservationUpdate(BaseModel):
    user_id: Optional[str] = None
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    start_time: Optional[datetime] = None
    note: Optional[str] = None
    status: Optional[ReservationStatus] = None