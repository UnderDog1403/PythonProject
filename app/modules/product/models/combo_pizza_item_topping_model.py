from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy import Column, Integer, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ComboPizzaItemTopping(Base):
    __tablename__ = "combo_pizza_item_topping"
    __table_args__ = (
        UniqueConstraint(
            "combo_pizza_item_id",
            "pizza_topping_id",
            name="uq_item_topping"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    combo_pizza_item_id = Column(
        Integer,
        ForeignKey("combo_pizza_items.id", ondelete="CASCADE"),
        nullable=False
    )
    pizza_topping_id = Column(
        Integer,
        ForeignKey("pizza_toppings.id"),
        nullable=False
    )
    is_actived = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    item = relationship(
        "ComboPizzaItem",
        back_populates="toppings"
    )
