from sqlalchemy import Integer, Column, String, Text, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base

class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    price = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    product = relationship("Product", back_populates="variants")
    variant_attributes = relationship(
        "VariantAttributeValue",
        back_populates="variant",
        cascade="all, delete-orphan"
    )

    attribute_values = relationship(
        "AttributeValue",
        secondary="variant_attribute_values",
        back_populates="variants"
    )
