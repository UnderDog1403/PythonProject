from sqlalchemy import Column, BigInteger, String, Numeric, Text, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import declarative_base, relationship

from app.core.database import Base

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)


    order_id = Column(BigInteger, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    product_variant_id = Column(BigInteger, ForeignKey("product_variants.id", ondelete="SET NULL"), nullable=True)

    product_name = Column(String(255), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)


    quantity = Column(Integer, nullable=False, default=1)
    note = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    order = relationship("Order", back_populates="items")
    options = relationship("OrderItemOption", back_populates="order_item", cascade="all, delete-orphan")