from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

# Replace this Base with your project's shared Base (e.g. from app.database import Base)
from app.core.database import Base

class PizzaCategoryMapping(Base):
    __tablename__ = "pizza_category_mapping"
    __table_args__ = (
        UniqueConstraint("pizza_id", "category_id", name="uq_pizza_category_mapping"),
    )
    id = Column(Integer, primary_key=True)
    pizza_id = Column(Integer, ForeignKey("pizzas.id",ondelete="CASCADE"),nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id",ondelete="CASCADE"),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    pizza = relationship("Pizza", back_populates="categories")
    category = relationship("Category", back_populates="pizzas")