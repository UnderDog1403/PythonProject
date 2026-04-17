from sqlalchemy import Column, ForeignKey, BigInteger, DateTime, func, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base
class VariantAttributeValue(Base):
    __tablename__ = "variant_attribute_values"

    variant_id = Column(
        Integer,
        ForeignKey("product_variants.id"),
        primary_key=True,
        nullable=False
    )

    attribute_value_id = Column(
        Integer,
        ForeignKey("attribute_values.id"),
        primary_key=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
