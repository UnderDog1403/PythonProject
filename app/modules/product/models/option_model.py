from sqlalchemy import Integer, Column, String, Text, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base
class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    min_select= Column(Integer, nullable=False, default=0)
    max_select = Column(Integer, nullable=False, default=100)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    values = relationship(
        "OptionValue",
        back_populates="option"
    )
    products = relationship(
        "Product",
        secondary="product_options",
        back_populates="options"
    )