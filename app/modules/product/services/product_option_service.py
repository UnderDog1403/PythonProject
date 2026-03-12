from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.repositories.product_option_repository import ProductOptionRepository
from app.modules.product.schemas.product_option_schema import ProductOptionResponseSchema




class ProductOptionService:
    def __init__(self, db: AsyncSession):
        self.repository = ProductOptionRepository(db)
    async def get_all(self)-> list[ProductOptionResponseSchema]:
        product_options = await self.repository.get_all()
        return product_options
    async def create(self, data: dict):
        try:
            product_option =await self.repository.create(data)
            return product_option
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while creating product_option"
            )
    async def delete(self,product_id, option_id):
        try:
            await self.repository.delete(product_id, option_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting product_option"
            )