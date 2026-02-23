# python
# modules/product/services/pizza_service.py
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from requests import Session

from app.modules.product.models.pizza_model import Pizza
from app.modules.product.repositories.pizza_repository import PizzaRepository

class PizzaService:
    def __init__(self, db: Session):
        self.repository = PizzaRepository(db)
    async def get_pizzas_paginated(
        self,
        page: int = 1,
        limit: int = 10,
        order_by: str = "id",
        descending: bool = False
    ):
        try:
            return await self.repository.get_pizzas_paginated(
                page=page,
                limit=limit,
                order_by=order_by,
                descending=descending
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while retrieving pizzas: {str(e)}"
            )
    async def create_pizza(self, data: dict) -> Pizza:
        try:
            return await self.repository.create(data)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating pizza: {str(e)}"
            )
    async def get_pizza_by_id(self, pizza_id: int) -> Pizza | None:
        try:
            pizza = await self.repository.get_pizza_by_id(pizza_id)
            if not pizza:
                raise HTTPException(
                    status_code=404,
                    detail=f"Pizza not found"
                )
            return pizza
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while retrieving pizza: {str(e)}"
            )
    async def update_pizza(self, pizza_id: int, data: dict) -> Pizza | None:
        try:
            pizza = await self.repository.update(pizza_id, data)
            if not pizza:
                raise HTTPException(
                    status_code=404,
                    detail=f"Pizza not found"
                )
            return pizza
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while updating pizza: {str(e)}"
            )
    async def delete_pizza(self, pizza_id: int) -> bool:
        try:
            success = await self.repository.delete(pizza_id)
            if not success:
                raise HTTPException(
                    status_code=404,
                    detail=f"Pizza not found"
                )
            return success
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while deleting pizza: {str(e)}"
            )
