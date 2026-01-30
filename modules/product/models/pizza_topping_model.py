from sqlalchemy import Column, Integer, String, Numeric, Boolean
from sqlalchemy.orm import declarative_base

# Replace this Base with your project's shared Base (e.g. from app.database import Base)
from core.database import Base

class PizzaTopping(Base):
    __tablename__ = "pizza_toppings"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_actived = Column(Boolean, nullable=False, default=True)