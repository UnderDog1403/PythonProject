from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.repositories.pizza_topping_repository import PizzaToppingRepository


class PizzaToppingService:
    def __init__(self, db: AsyncSession):
        self.repository = PizzaToppingRepository(db)

    async def get_all_pizza_toppings(self):
        try:
            pizza_toppings = await self.repository.get_all()
            return pizza_toppings
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving pizza toppings"
            )

    async def create_pizza_topping(self, data: dict):
        try:
            pizza_topping = await self.repository.create(data)
            return pizza_topping
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while creating pizza topping"
            )

    async def update_pizza_topping(self, pizza_topping_id: int, data: dict):
        try:
            pizza_topping = await self.repository.update(pizza_topping_id, data)
            if not pizza_topping:
                raise HTTPException(status_code=404, detail="Pizza topping not found")
            return pizza_topping
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while updating pizza topping"
            )

    async def delete_pizza_topping(self, pizza_topping_id: int):
        try:
            deleted = await self.repository.delete(pizza_topping_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Pizza topping not found")
            return deleted
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting pizza topping"
            )
