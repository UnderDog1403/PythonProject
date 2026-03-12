from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.product.repositories.variant_attribute_value_repositoy import VariantAttributeValueRepository
from app.modules.product.schemas.variant_attribute_value_schema import VariantAttributeValueResponseSchema




class VariantAttributeValueService:
    def __init__(self, db: AsyncSession):
        self.repository = VariantAttributeValueRepository(db)
    async def get_all(self)-> list[VariantAttributeValueResponseSchema]:
        variant_attribute_values = await self.repository.get_all()
        return variant_attribute_values
    async def create(self, data: dict):
        try:
            variant_attribute_value =await self.repository.create(data)
            return variant_attribute_value
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while creating variant_attribute_value"
            )
    async def delete(self,variant_id, attribute_value_id):
        try:
            await self.repository.delete(variant_id, attribute_value_id)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting variant_attribute_value"
            )