
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.modules.product.models.pizza_category_mapping_model import PizzaCategoryMapping
# Replace this Base with your project's shared Base (e.g. from app.database import Base)
from app.core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_actived = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    pizzas = relationship("PizzaCategoryMapping", back_populates="category", cascade="all, delete-orphan",passive_deletes=True)