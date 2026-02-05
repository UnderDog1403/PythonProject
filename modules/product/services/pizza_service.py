# python
# modules/product/services/pizza_service.py
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from requests import Session

from modules.product.models.pizza_model import Pizza
from modules.product.repositories.pizza_repository import PizzaRepository

class PizzaService:
    def __init__(self, db: Session):
        self.repository = PizzaRepository(db)

    def get_pizzas_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "id",
        descending: bool = False,
    ) -> Tuple[List[Pizza], int, int]:
        # validate inputs
        if page < 1 or limit < 1:
            raise HTTPException(status_code=400, detail="`page` and `limit` must be positive integers")
        try:
            items, total, total_pages = self.repository.get_pizzas_paginated(
                page=page, limit=limit, order_by=order_by, descending=descending
            )
            return items, total, total_pages
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving pizzas"
            )
    def get_active_pizzas_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "id",
        descending: bool = False,
    ) -> Tuple[List[Pizza], int, int]:
        # validate inputs
        if page < 1 or limit < 1:
            raise HTTPException(status_code=400, detail="`page` and `limit` must be positive integers")
        try:
            pizzas, total, total_pages = self.repository.get_active_pizzas_paginated(
                page=page, limit=limit, order_by=order_by, descending=descending
            )
            return pizzas, total, total_pages
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving pizzas"
            )
    def get_pizza_by_id(self, pizza_id: int) -> Optional[Pizza]:
        if not isinstance(pizza_id, int) or pizza_id < 1:
            raise HTTPException(status_code=400, detail="\`pizza_id\` must be a positive integer")
        try:
            pizza = self.repository.get_pizza_by_id(pizza_id)
            if not pizza:
                raise HTTPException(status_code=404, detail="Pizza not found")
            return pizza
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving pizza"
            )
    def update_pizza(self, pizza_id: int, data: Dict[str, Any]):
        if not isinstance(pizza_id, int) or pizza_id < 1:
            raise HTTPException(status_code=400, detail="\`pizza_id\` must be a positive integer")
        try:
            updated = self.repository.update_pizza(pizza_id, data)
            if not updated:
                raise HTTPException(status_code=404, detail="Pizza not found")
            return updated
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while updating pizza"
            )
    def create_pizza(self, data: Dict[str, Any]) -> Pizza:
        if not data.get("name"):
            raise ValueError("Pizza name is required")
        if data.get("base_price", 0) <= 0:
            raise ValueError("Base price must be greater than 0")
        return self.repository.create_pizza(data)
    def delete_pizza(self, pizza_id: int) -> bool:
        if not isinstance(pizza_id, int) or pizza_id < 1:
            raise HTTPException(status_code=400, detail="\`pizza_id\` must be a positive integer")
        try:
            deleted = self.repository.delete_pizza(pizza_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Pizza not found")
            return deleted
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting pizza"
            )
    def search_active_pizzas_paginated(
        self,
        keyword: Optional[str],
        page: int = 1,
        limit: int = 10,
        order_by: str = "id",
        descending: bool = False,
    ) -> Tuple[List[Pizza], int, int]:
        # validate inputs
        if page < 1 or limit < 1:
            raise HTTPException(status_code=400, detail="`page` and `limit` must be positive integers")
        try:
            pizzas, total, total_pages = self.repository.search_active_pizzas_paginated(
                keyword=keyword,
                page=page,
                limit=limit,
                order_by=order_by,
                descending=descending
            )
            return pizzas, total, total_pages
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while searching pizzas"
            )

