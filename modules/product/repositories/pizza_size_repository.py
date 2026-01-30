## python
# modules/product/repositories/pizza_size_repository.py
from typing import List, Optional, Any, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from modules.product.models.pizza_size_model import PizzaSize

class PizzaSizeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_categories_paginated(self, page: int = 1, limit: int = 10, order_by: str = "id",
                                 descending: bool = False) -> Tuple[List[PizzaSize], int, int]:
        offset_value = max(page - 1, 0) * limit
        order_col = getattr(PizzaSize, order_by, PizzaSize.id)
        order_fn = desc if descending else asc

        total = self.db.query(PizzaSize).count()

        items = (
            self.db.query(PizzaSize)
            .order_by(order_fn(order_col))
            .offset(offset_value)
            .limit(limit)
            .all()
        )

        total_pages = (total + limit - 1) // limit if limit > 0 else 0

        return items, total, total_pages

    def get_pizza_size_by_id(self, pizza_size_id: int) -> Optional[PizzaSize]:
        return self.db.query(PizzaSize).filter(PizzaSize.id == pizza_size_id).one_or_none()

    def create_pizza_size(self, name: str, description: Optional[str] = None) -> PizzaSize:
        pizza_size = PizzaSize(name=name, description=description)
        self.db.add(pizza_size)
        self.db.commit()
        self.db.refresh(pizza_size)
        return pizza_size

    def update_pizza_size(self, pizza_size_id: int, data: Dict[str, Any]) -> Optional[PizzaSize]:
        pizza_size = self.get_pizza_size_by_id(pizza_size_id)
        if not pizza_size:
            return None
        for key, value in data.items():
            if key == "id":
                continue
            if hasattr(pizza_size, key):
                setattr(pizza_size, key, value)
        self.db.commit()
        self.db.refresh(pizza_size)
        return pizza_size

    def delete_pizza_size(self, pizza_size_id: int) -> bool:
        pizza_size = self.get_pizza_size_by_id(pizza_size_id)
        if not pizza_size:
            return False
        self.db.delete(pizza_size)
        self.db.commit()
        return True