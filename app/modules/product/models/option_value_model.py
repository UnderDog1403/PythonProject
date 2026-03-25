from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

# Replace this Base with your project's shared Base (e.g. from app.database import Base)
from app.core.database import Base


class OptionValue(Base):
    __tablename__ = "option_values"
    __table_args__ = (
        UniqueConstraint("option_id", "value", name="uq_option_value"),
    )
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    option_id = Column(Integer, ForeignKey("options.id"), nullable=False)
    value = Column(String(255), nullable=False)
    extra_price = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    option = relationship("Option",lazy="selectin", back_populates="values")


