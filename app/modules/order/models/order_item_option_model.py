from sqlalchemy import Column, BigInteger, String, Numeric, Text, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import declarative_base, relationship

from app.core.database import Base
class OrderItemOption(Base):
    __tablename__ = "order_item_options"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)

    order_item_id = Column(BigInteger, ForeignKey("order_items.id", ondelete="CASCADE"), nullable=False, index=True)

    option_id = Column(BigInteger, ForeignKey("options.id", ondelete="SET NULL"), nullable=True)
    option_value_id = Column(BigInteger, ForeignKey("option_values.id", ondelete="SET NULL"), nullable=True)


    option_name = Column(String(100), nullable=False)       # VD: "Size", "Lượng đá", "Topping"
    option_value_name = Column(String(100), nullable=False) # VD: "L", "50%", "Trân châu trắng"
    extra_price = Column(Numeric(12, 2), default=0)         # Tiền cộng thêm lúc mua (VD: Size L +10k)


    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # --- Relationships ---
    order_item = relationship("OrderItem", back_populates="options")