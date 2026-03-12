from sqlalchemy import Integer, Column, String, Text, ForeignKey, Boolean, DateTime, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class AttributeValue(Base):
    __tablename__ = "attribute_values"
    __table_args__ = (
        UniqueConstraint("attribute_id", "value", name="uq_attribute_value"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    attribute_id = Column(Integer, ForeignKey("attributes.id"), nullable=False)
    value = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    attribute = relationship(
        "Attribute",
        back_populates="values"
    )
    variant_links = relationship(
        "VariantAttributeValue",
        back_populates="attribute_value"
    )
    variants = relationship(
        "ProductVariant",
        secondary="variant_attribute_values",
        back_populates="attribute_values"
    )