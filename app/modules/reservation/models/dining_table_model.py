from enum import Enum

from sqlalchemy import Integer, Column, String, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.core.database import Base


class DiningTable(Base):
    __tablename__ = "dining_tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    capacity = Column(Integer, default=4) # Vẫn giữ sức chứa mặc định là 4
    reservations = relationship(
        "Reservation",
        secondary="reservation_tables",
        back_populates="tables"
    )
    reservation_links = relationship("ReservationTable", back_populates="dining_table")