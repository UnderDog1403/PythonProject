# modules/product/services/product_service.py
import json
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.modules.product.models.product_model import Product
from app.modules.product.repositories.product_repostiory import ProductRepository
from app.modules.product.schemas.product_schema import ProductResponseSchema, ProductDetailResponseSchema


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repository = ProductRepository(db)
    async def get_all(self)-> list[ProductResponseSchema]:
        cached_item = await redis_client.get(f"items:products:all")
        if cached_item:
            data = json.loads(cached_item)
            return TypeAdapter(List[ProductResponseSchema]).validate_python(data)
        # try:
        products = await self.repository.get_all()
        products_data = []
        for product in products:
            price = min(v.price for v in product.variants) if product.variants else None
            products_data.append({
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "image_url": product.image_url,
                "category_id": product.category_id,
                "is_active": product.is_active,
                "price": price
            })
        await redis_client.set(
                f"items:products:all",
                json.dumps(products_data),
                ex=3600  # cache for 1 hour
            )
        return TypeAdapter(List[ProductResponseSchema]).validate_python(products_data)
        # except Exception:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Internal server error while retrieving products"
        #     )
    # async def get_products_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False,
    # ) -> Tuple[List[Product], int, int]:
    #
    #     # validate inputs
    #     if page < 1 or limit < 1:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="`page` and `limit` must be positive integers"
    #         )
    #
    #     try:
    #         items, total, total_pages = await self.repository.get_products_paginated(
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
    #             detail="Internal server error while retrieving products"
    #         )
    async def get_by_id(self, product_id: int) -> Optional[ProductDetailResponseSchema]:
        cache_key = f"items:products:{product_id}"
        cached_item = await redis_client.get(cache_key)
        if cached_item:
            data = json.loads(cached_item)
            return TypeAdapter(ProductDetailResponseSchema).validate_python(data)
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
        price = min(v.price for v in product.variants) if product.variants else None
        variants_data = [
            {
                "id": v.id,
                "product_id": v.product_id,
                "price": v.price,
                "is_active": v.is_active,
                "attribute_value_ids": [val.id for val in v.attribute_values]
            }
            for v in product.variants
        ] if product.variants else []
        attributes_map = {}

        for variant in product.variants:
            for value in variant.attribute_values:
                attr = value.attribute

                if attr.id not in attributes_map:
                    attributes_map[attr.id] = {
                        "id": attr.id,
                        "name": attr.name,
                        "values": [],
                        "is_active": attr.is_active
                    }

                if value.id not in [v["id"] for v in attributes_map[attr.id]["values"]]:
                    attributes_map[attr.id]["values"].append({
                        "id": value.id,
                        "attribute_id": value.attribute_id,
                        "value": value.value,
                        "is_active": value.is_active
                    })

        attributes_data = list(attributes_map.values())
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "image_url": product.image_url,
            "category_id": product.category_id,
            "is_active": product.is_active,
            "price": price,
            "variants": variants_data,
            "attributes": attributes_data
        }
        # 6. Cache Redis
        await redis_client.set(
            cache_key,
            json.dumps(product_data),
            ex=3600
        )

        # 7. Return schema
        return TypeAdapter(ProductDetailResponseSchema).validate_python(product_data)

    async def create(self, data: dict):
        try:
            product =await self.repository.create(data)
            await redis_client.delete("items:products:all")
            return product
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating pizza: {str(e)}"
            )
    async def update(self, product_id: int, data: dict):
        try:
            product = await self.repository.update(product_id, data)
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product not found"
                )
            await redis_client.delete("items:products:all")
            return product
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while updating pizza: {str(e)}"
            )
    async def delete(self, product_id: int) -> bool:
        try:
            deleted = await self.repository.delete(product_id)
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )
            await redis_client.delete("items:products:all")
            return True
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting product"
            )
