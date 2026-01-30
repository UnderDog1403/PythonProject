# python
# modules/product/services/category_service.py
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from requests import Session

from modules.product.models.category_model import Category
from modules.product.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)

    def get_categories_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "id",
        descending: bool = False,
    ) -> Tuple[List[Category], int, int]:
        # validate inputs
        if page < 1 or limit < 1:
            raise HTTPException(status_code=400, detail="`page` and `limit` must be positive integers")
        try:
            items, total, total_pages = self.repository.get_categories_paginated(
                page=page, limit=limit, order_by=order_by, descending=descending
            )
            return items, total, total_pages
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving categories"
            )

    def create_category(self, name: str, description: Optional[str] = None) -> Category:
        if not name or not isinstance(name, str) or not name.strip():
            raise HTTPException(status_code=400, detail="\`name\` is required and must be a non-empty string")
        try:
            category = self.repository.create_category(name=name.strip(), description=description)
            return category
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while creating category"
            )

    def update_category(self, category_id: int, data: Dict[str, Any]):
        if not isinstance(category_id, int) or category_id < 1:
            raise HTTPException(status_code=400, detail="\`category_id\` must be a positive integer")
        if not isinstance(data, dict) or not data:
            raise HTTPException(status_code=400, detail="\`data\` must be a non-empty object with fields to update")
        # Prevent updating the id field
        data = {k: v for k, v in data.items() if k != "id"}
        try:
            updated = self.repository.update_category(category_id, data)
            if not updated:
                raise HTTPException(status_code=404, detail="Category not found")
            return updated
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while updating category"
            )

