from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class PizzaSizeMapping(Base):
    __tablename__ = "pizza_sizes_mapping"
    __table_args__ = (
        UniqueConstraint("pizza_id", "size_id", name="uq_pizza_size_mapping"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    pizza_id = Column(Integer, ForeignKey("pizzas.id", ondelete="CASCADE"), nullable=False)
    size_id = Column(Integer, ForeignKey("pizza_sizes.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    pizza = relationship("Pizza", back_populates="sizes")
    size = relationship("PizzaSize", back_populates="pizzas")

