from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class ReservationTable(Base):
    __tablename__ = "reservation_tables"

    dining_table_id = Column(Integer, ForeignKey("dining_tables.id"), primary_key=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), primary_key=True)

    dining_table = relationship("DiningTable", back_populates="reservation_links")
    reservation = relationship("Reservation", back_populates="table_links")

