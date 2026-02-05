from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base

# Replace this Base with your project's shared Base (e.g. from app.database import Base)
from core.database import Base

class PizzaCategory(Base):
    __tablename__ = "pizza_category"

    id = Column(Integer, primary_key=True)
    pizza_id = Column(Integer, ForeignKey("pizzas.id",ondelete="CASCADE"),nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )