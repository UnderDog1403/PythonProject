from sqlalchemy import Column, Integer, String, Text, Boolean, Numeric, DateTime, func

from app.core.database import Base
class Combo(Base):
    __tablename__ = "combo"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    price = Column(Numeric(10, 2), nullable=False)
    discount_percent = Column(Integer, default=0)

    is_actived = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )