from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func
from sqlalchemy.orm import declarative_base

# Replace this Base with your project's shared Base (e.g. from app.database import Base)
from core.database import Base

class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    image = Column(String(1024), nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)
    is_actived = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )