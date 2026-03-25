import enum

from sqlalchemy import Column, BigInteger, String, Numeric, Text, DateTime, Enum as SQLEnum, func, ForeignKey, UUID
from sqlalchemy.orm import declarative_base, relationship

from app.core.database import Base


class DeliveryType(str, enum.Enum):
    PICKUP = "PICKUP"
    DELIVERY = "DELIVERY"


class PaymentMethod(str, enum.Enum):
    ONLINE = "ONLINE"
    COD = "COD"


class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    


class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    DELIVERING = "DELIVERING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Order(Base):
    __tablename__ = "orders"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    voucher_id = Column(BigInteger, ForeignKey("vouchers.id", ondelete="SET NULL"), nullable=True)

    subtotal = Column(Numeric(12, 2), nullable=False)  # Tiền trước giảm
    discount_amount = Column(Numeric(12, 2), default=0)  # Tiền giảm từ voucher
    shipping_fee = Column(Numeric(12, 2), default=0)  # Phí ship
    total_amount = Column(Numeric(12, 2), nullable=False)  # Tiền thanh toán cuối cùng

    customer_name = Column(String(255), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    voucher_code = Column(String(50), nullable=True)

    delivery_type = Column(SQLEnum(DeliveryType, native_enum=False, length=20), nullable=False)
    pickup_time = Column(DateTime(timezone=True), nullable=True)
    delivery_address = Column(Text, nullable=True)


    payment_method = Column(SQLEnum(PaymentMethod, native_enum=False, length=20), nullable=False)
    payment_status = Column(SQLEnum(PaymentStatus, native_enum=False, length=20), default=PaymentStatus.PENDING)
    status = Column(SQLEnum(OrderStatus, native_enum=False, length=20), default=OrderStatus.PENDING)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    user = relationship("User", back_populates="orders")
    voucher = relationship("Voucher", back_populates="orders")


    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")