import enum
import uuid
from sqlalchemy import Column, String, Boolean, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

class UserRoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    # password = Column(String, nullable=False)
    role = Column(
        Enum(UserRoleEnum, name="user_role_enum"),
        nullable=False,
        server_default="user"
    )
    address = Column(String, nullable=True)
    image = Column(String, nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    auth_providers = relationship(
        "AuthProvider",
        back_populates="user",
        cascade="all, delete"
    )