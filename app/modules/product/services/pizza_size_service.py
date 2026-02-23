from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.repositories.pizza_size_repository import PizzaSizeRepository


class PizzaSizeService:
    def __init__(self, db: AsyncSession):
        self.repository = PizzaSizeRepository(db)

    async def get_all_pizza_sizes(self):
        try:
            pizza_sizes = await self.repository.get_all()
            return pizza_sizes
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving pizza sizes"
            )

    async def create_pizza_size(self, data: dict):
        try:
            pizza_size = await self.repository.create(data)
            return pizza_size
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while creating pizza size"
            )
    async def update_pizza_size(self, pizza_size_id: int, data: dict):
        try:
            pizza_size = await self.repository.update(pizza_size_id, data)
            if not pizza_size:
                raise HTTPException(status_code=404, detail="Pizza size not found")
            return pizza_size
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while updating pizza size"
            )
    async def delete_pizza_size(self, pizza_size_id: int):
        try:
            deleted = await self.repository.delete(pizza_size_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Pizza size not found")
            return deleted
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting pizza size"
            )
