from sqlalchemy import Column, String, DateTime
import uuid
from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    jti = Column(String, unique=True, index=True)
    expired_at = Column(DateTime)
