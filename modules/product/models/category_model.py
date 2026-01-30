
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import declarative_base

# Replace this Base with your project's shared Base (e.g. from app.database import Base)
from core.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_actived = Column(Boolean, nullable=False, default=True)