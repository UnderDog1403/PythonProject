# modules/product/services/product_service.py
import json
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.modules.product.models.product_model import Product
from app.modules.product.models.product_variant_model import ProductVariant
from app.modules.product.repositories.attribute_value_repository import AttributeValueRepository
from app.modules.product.repositories.option_repository import OptionRepository
from app.modules.product.repositories.product_option_repository import ProductOptionRepository
from app.modules.product.repositories.product_repostiory import ProductRepository
from app.modules.product.repositories.product_variant_repository import ProductVariantRepository
from app.modules.product.schemas.product_schema import ProductResponseSchema, ProductDetailResponseSchema


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repository = ProductRepository(db)
        self.db = db
        self.product_options_repo = ProductOptionRepository(db)
        self.option_repo = OptionRepository(db)
        self.variant_repo = ProductVariantRepository(db)
        self.attribute_value_repo = AttributeValueRepository(db)
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
            # 1. Khởi tạo đối tượng Product trên RAM
            product_dict = {
                "name": data.get("name"),
                "description": data.get("description"),
                "category_id": data.get("category_id"),
                "image_url": data.get("image_url")
            }
            product = Product(**product_dict)

            # 2. Trích xuất và gắn danh sách Options
            option_ids = data.get("options")
            if option_ids:
                options = await self.option_repo.get_by_ids(option_ids)
                product.options = options

            # 3. Trích xuất và gắn danh sách Variants
            variants = data.get("variants", [])
            for variant_data in variants:
                # TẠO TRÊN RAM, KHÔNG GỌI REPO CREATE
                # Không cần truyền product_id, SQLAlchemy sẽ tự map qua relationship!
                variant = ProductVariant(
                    price=variant_data.get("price"),
                    is_active=variant_data.get("is_active")
                )

                # Gắn Attributes vào Variant
                attribute_value_ids = variant_data.get("attribute_value_ids")
                if attribute_value_ids:
                    attribute_values = await self.attribute_value_repo.get_by_ids(attribute_value_ids)
                    variant.attribute_values = attribute_values

                # DÙNG APPEND ĐỂ THÊM VÀO DANH SÁCH VARIANTS CỦA PRODUCT
                product.variants.append(variant)

            # 4. LƯU TOÀN BỘ XUỐNG DB 1 LẦN DUY NHẤT
            # Tùy thuộc cấu trúc code của bạn, dùng thẳng db session cho an toàn:
            self.repository.db.add(product)
            await self.repository.db.commit()
            await self.repository.db.refresh(product)

            # Xóa cache Redis
            await redis_client.delete("items:products:all")

            return product

        except Exception as e:
            await self.repository.db.rollback()
            print(f"Error creating product: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating product: {str(e)}"
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
