from sqlalchemy import Column, BigInteger, String, Numeric, Integer, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.schema import Identity
from app.core.database import Base


class Voucher(Base):
    __tablename__ = "vouchers"
    id = Column(
        Integer,
        Identity(always=True),
        primary_key=True,
        nullable=False
    )
    code = Column(String(255), nullable=False, unique=True)
    discount_type = Column(
        Enum("fixed", "percent", name="discount_type_enum"),
        nullable=False
    )
    discount_value = Column(Numeric(15, 2), nullable=False)
    min_order_value = Column(Numeric(15, 2), default=0)
    max_discount_value = Column(Numeric(15, 2), nullable=True)
    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=False)
    usage_limit = Column(Integer, nullable=False, default=0)

    used_count = Column(Integer, nullable=False, default=0)

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    orders = relationship("Order", back_populates="voucher")