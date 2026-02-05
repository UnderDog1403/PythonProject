from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from core.database import Base


class ComboPizzaItemSize(Base):
    __tablename__ = "combo_pizza_item_size"
    __table_args__ = (
        UniqueConstraint("combo_pizza_item_id", name="uq_item_size"),
    )

    id = Column(Integer, primary_key=True, index=True)
    combo_pizza_item_id = Column(
        Integer,
        ForeignKey("combo_pizza_items.id", ondelete="CASCADE"),
        nullable=False
    )
    pizza_size_id = Column(
        Integer,
        ForeignKey("pizza_sizes.id"),
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
        back_populates="sizes"
    )
