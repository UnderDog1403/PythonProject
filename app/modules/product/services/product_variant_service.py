# modules/product_variant/services/product_variant_service.py
import json
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.modules.product.models.product_variant_model import ProductVariant
from app.modules.product.repositories.product_variant_repository import ProductVariantRepository
from app.modules.product.schemas.product_variant_schema import ProductVariantResponseSchema


class ProductVariantService:
    def __init__(self, db: AsyncSession):
        self.repository = ProductVariantRepository(db)
    async def get_all_by_product_id(self, product_id: int)-> list[ProductVariantResponseSchema]:

        # try:
        variants = await self.repository.get_all_by_product_id(product_id)

        result = []

        for v in variants:
            result.append(
                ProductVariantResponseSchema(
                    id=v.id,
                    price=v.price,
                    product_id=v.product_id,
                    attribute_value_ids=[
                        av.id for av in v.attribute_values
                    ],
                    is_active=v.is_active
                )
            )

        return result
        # except Exception:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Internal server error while retrieving product_variants"
        #     )
    # async def get_product_variants_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False,
    # ) -> Tuple[List[ProductVariant], int, int]:
    #
    #     # validate inputs
    #     if page < 1 or limit < 1:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="`page` and `limit` must be positive integers"
    #         )
    #
    #     try:
    #         items, total, total_pages = await self.repository.get_product_variants_paginated(
    #             page=page,
    #             limit=limit,
    #             order_by=order_by,
    #             descending=descending,
    #         )
    #         return items, total, total_pages
    #     except HTTPException:
    #         raise
    #     except Exception:
    #         raise HTTPException(
    #             status_code=500,
    #             detail="Internal server error while retrieving product_variants"
    #         )

    async def create(self, data: dict):
        try:
            product_variant =await self.repository.create(data)

            return product_variant
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating pizza: {str(e)}"
            )
    async def update(self, product_variant_id: int, data: dict):
        try:
            product_variant = await self.repository.update(product_variant_id, data)
            if not product_variant:
                raise HTTPException(
                    status_code=404,
                    detail=f"ProductVariant not found"
                )

            return product_variant
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while updating pizza: {str(e)}"
            )
    async def delete(self, product_variant_id: int) -> bool:
        try:
            deleted = await self.repository.delete(product_variant_id)
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="ProductVariant not found"
                )

            return True
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting product_variant"
            )
