## python
# modules/product/repositories/pizza_repository.py
from typing import List, Optional, Any, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from modules.product.models.pizza_model import Pizza

class PizzaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_categories_paginated(self, page: int = 1, limit: int = 10, order_by: str = "id",
                                 descending: bool = False) -> Tuple[List[Pizza], int, int]:
        offset_value = max(page - 1, 0) * limit
        order_col = getattr(Pizza, order_by, Pizza.id)
        order_fn = desc if descending else asc

        total = self.db.query(Pizza).count()

        items = (
            self.db.query(Pizza)
            .order_by(order_fn(order_col))
            .offset(offset_value)
            .limit(limit)
            .all()
        )

        total_pages = (total + limit - 1) // limit if limit > 0 else 0

        return items, total, total_pages

    def get_pizza_by_id(self, pizza_id: int) -> Optional[Pizza]:
        return self.db.query(Pizza).filter(Pizza.id == pizza_id).one_or_none()

    def create_pizza(self, name: str, description: Optional[str] = None) -> Pizza:
        pizza = Pizza(name=name, description=description)
        self.db.add(pizza)
        self.db.commit()
        self.db.refresh(pizza)
        return pizza

    def update_pizza(self, pizza_id: int, data: Dict[str, Any]) -> Optional[Pizza]:
        pizza = self.get_pizza_by_id(pizza_id)
        if not pizza:
            return None
        for key, value in data.items():
            if key == "id":
                continue
            if hasattr(pizza, key):
                setattr(pizza, key, value)
        self.db.commit()
        self.db.refresh(pizza)
        return pizza

    def delete_pizza(self, pizza_id: int) -> bool:
        pizza = self.get_pizza_by_id(pizza_id)
        if not pizza:
            return False
        self.db.delete(pizza)
        self.db.commit()
        return True