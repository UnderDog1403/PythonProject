import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum
class AuthProviderEnum(str, enum.Enum):
    local = "local"
    google = "google"
    facebook = "facebook"

class AuthProvider(Base):
    __tablename__ = "auth_providers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    provider = Column(
        Enum(AuthProviderEnum, name="auth_provider_enum"),
        nullable=False
    )
    provider_user_id = Column(String(255), nullable=True)
    password_hash = Column(String(255), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    user = relationship(
        "User",
        back_populates="auth_providers"
    )