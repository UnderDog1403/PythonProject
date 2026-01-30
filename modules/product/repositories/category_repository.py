# python
# modules/product/repositories/category_repository.py
from typing import List, Optional, Any, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from modules.product.models.category_model import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_categories_paginated(self, page: int = 1, limit: int = 10, order_by: str = "id",
                                 descending: bool = False) -> Tuple[List[Category], int, int]:
        offset_value = max(page - 1, 0) * limit
        order_col = getattr(Category, order_by, Category.id)
        order_fn = desc if descending else asc

        total = self.db.query(Category).count()

        items = (
            self.db.query(Category)
            .order_by(order_fn(order_col))
            .offset(offset_value)
            .limit(limit)
            .all()
        )

        total_pages = (total + limit - 1) // limit if limit > 0 else 0

        return items, total, total_pages

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id).one_or_none()

    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        category = Category(name=name, description=description)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update_category(self, category_id: int, data: Dict[str, Any]) -> Optional[Category]:
        category = self.get_category_by_id(category_id)
        if not category:
            return None
        for key, value in data.items():
            if key == "id":
                continue
            if hasattr(category, key):
                setattr(category, key, value)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete_category(self, category_id: int) -> bool:
        category = self.get_category_by_id(category_id)
        if not category:
            return False
        self.db.delete(category)
        self.db.commit()
        return True