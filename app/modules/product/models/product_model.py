from sqlalchemy import Integer, Column, String, Text, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    image_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    variants = relationship("ProductVariant", back_populates="product")
    options = relationship(
        "Option",
        secondary="product_options",
        back_populates="products",
        lazy="selectin"
    )
