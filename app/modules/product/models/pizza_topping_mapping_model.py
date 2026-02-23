from sqlalchemy import DateTime, Column, Integer, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class PizzaToppingMapping(Base):
    __tablename__ = 'pizza_topping_mapping'
    __table_args__ = (
        UniqueConstraint('pizza_id', 'topping_id', name='uq_pizza_topping_mapping'),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    pizza_id = Column(Integer, ForeignKey('pizzas.id',ondelete="CASCADE"), nullable=False)
    topping_id = Column(Integer, ForeignKey('pizza_toppings.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    pizza = relationship("Pizza", back_populates="toppings")
    topping = relationship("PizzaTopping", back_populates="pizzas")