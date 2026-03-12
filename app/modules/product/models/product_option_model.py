from sqlalchemy import Column, Integer, ForeignKey, func, DateTime

from app.core.database import Base


class ProductOption(Base):
    __tablename__ = "product_options"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, primary_key=True)
    option_id = Column(Integer, ForeignKey("options.id"), nullable=False, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())