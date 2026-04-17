from enum import Enum

from sqlalchemy import Column, BigInteger, String, Numeric, Text, DateTime, Enum as SQLEnum, func, ForeignKey, UUID, \
    Integer
from sqlalchemy.orm import declarative_base, relationship

from app.core.database import Base
class ReservationStatus(str, Enum):
    PENDING = "pending"        # chờ xác nhận (nếu cần staff duyệt)
    CONFIRMED = "confirmed"    # đã xác nhận
    CHECKED_IN = "checked_in"  # khách đã đến
    COMPLETED = "completed"    # đã hoàn thành (khách đã rời đi)
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
class ReservationSource(str, Enum):
    ONLINE = "online"          # đặt qua website/app
    POS = "pos"            # đặt qua điện thoại
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)


    user_id = Column(String(100), nullable=True)
    customer_name = Column(String(100), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    source = Column(
        SQLEnum(
            ReservationSource,
            native_enum=False  # quan trọng → postgres lưu dạng VARCHAR
        ),
        default=ReservationSource.ONLINE,
        index=True,
        nullable=False
    )
    guest_count = Column(Integer, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    status = Column(
        SQLEnum(
            ReservationStatus,
            native_enum=False  # quan trọng → postgres lưu dạng VARCHAR
        ),
        default=ReservationStatus.PENDING,
        index=True,
        nullable=False
    )
    note = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    tables = relationship(
        "DiningTable",
        secondary= "reservation_tables",
        back_populates="reservations"
    )
    table_links = relationship("ReservationTable", back_populates="reservation")