from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.modules.product.models.pizza_size_mapping_model import PizzaSizeMapping
# Replace this Base with your project's shared Base (e.g. from app.database import Base)
from app.core.database import Base

class PizzaSize(Base):
    __tablename__ = "pizza_sizes"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String(100), nullable=False, unique=True)
    coefficient_price = Column(Numeric(5, 2), nullable=False)
    is_actived = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    pizzas = relationship("PizzaSizeMapping", back_populates="size", cascade="all, delete-orphan",passive_deletes=True)