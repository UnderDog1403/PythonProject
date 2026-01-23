import uuid
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func
from core.database import Base
import enum
class PasswordReset(Base):
    __tablename__ = "password_resets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    email = Column(
        String(255),
        nullable=False,
        index=True
    )

    otp_hash = Column(
        String(255),
        nullable=False
    )

    expired_at = Column(
        DateTime,
        nullable=False
    )
    is_used = Column(
        Boolean,
        default=False,
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
