from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base
class ComboPizzaItem(Base):
    __tablename__ = "combo_pizza_items"

    id = Column(Integer, primary_key=True, index=True)
    combo_id = Column(
        Integer,
        ForeignKey("combo.id", ondelete="CASCADE"),
        nullable=False
    )
    pizza_id = Column(
        Integer,
        ForeignKey("pizzas.id"),
        nullable=False
    )
    is_actived = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # relationships
    sizes = relationship(
        "ComboPizzaItemSize",
        back_populates="item",
        cascade="all, delete-orphan"
    )

    toppings = relationship(
        "ComboPizzaItemTopping",
        back_populates="item",
        cascade="all, delete-orphan"
    )
