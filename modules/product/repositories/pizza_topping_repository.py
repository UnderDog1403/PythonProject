## python
# modules/product/repositories/pizza_topping_repository.py
from typing import List, Optional, Any, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from modules.product.models.pizza_topping_model import PizzaTopping

class PizzaToppingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_categories_paginated(self, page: int = 1, limit: int = 10, order_by: str = "id",
                                 descending: bool = False) -> Tuple[List[PizzaTopping], int, int]:
        offset_value = max(page - 1, 0) * limit
        order_col = getattr(PizzaTopping, order_by, PizzaTopping.id)
        order_fn = desc if descending else asc

        total = self.db.query(PizzaTopping).count()

        items = (
            self.db.query(PizzaTopping)
            .order_by(order_fn(order_col))
            .offset(offset_value)
            .limit(limit)
            .all()
        )

        total_pages = (total + limit - 1) // limit if limit > 0 else 0

        return items, total, total_pages

    def get_pizza_topping_by_id(self, pizza_topping_id: int) -> Optional[PizzaTopping]:
        return self.db.query(PizzaTopping).filter(PizzaTopping.id == pizza_topping_id).one_or_none()

    def create_pizza_topping(self, name: str, description: Optional[str] = None) -> PizzaTopping:
        pizza_topping = PizzaTopping(name=name, description=description)
        self.db.add(pizza_topping)
        self.db.commit()
        self.db.refresh(pizza_topping)
        return pizza_topping

    def update_pizza_topping(self, pizza_topping_id: int, data: Dict[str, Any]) -> Optional[PizzaTopping]:
        pizza_topping = self.get_pizza_topping_by_id(pizza_topping_id)
        if not pizza_topping:
            return None
        for key, value in data.items():
            if key == "id":
                continue
            if hasattr(pizza_topping, key):
                setattr(pizza_topping, key, value)
        self.db.commit()
        self.db.refresh(pizza_topping)
        return pizza_topping

    def delete_pizza_topping(self, pizza_topping_id: int) -> bool:
        pizza_topping = self.get_pizza_topping_by_id(pizza_topping_id)
        if not pizza_topping:
            return False
        self.db.delete(pizza_topping)
        self.db.commit()
        return True