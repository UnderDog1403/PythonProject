# modules/product/services/product_service.py
import json
from typing import Tuple, List, Dict, Any, Optional, Coroutine, Sequence
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
from app.modules.product.repositories.variant_attribute_value_repositoy import VariantAttributeValueRepository
from app.modules.product.schemas.product_schema import ProductResponseSchema, ProductDetailResponseSchema


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repository = ProductRepository(db)
        self.db = db
        self.product_options_repo = ProductOptionRepository(db)
        self.option_repo = OptionRepository(db)
        self.variant_repo = ProductVariantRepository(db)
        self.attribute_value_repo = AttributeValueRepository(db)
        self.variant_attribute_value_repo = VariantAttributeValueRepository(db)
    async def get_all(self)-> list[ProductResponseSchema]:
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
    async def admin_get_all(self) -> Sequence[Product]:
        products = await self.repository.admin_get_all()
        return products
    async def get_by_id(self, product_id: int) -> Optional[ProductDetailResponseSchema]:
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
        options_data = [
            {
                "id": opt.id,
                "name": opt.name,
                "min_select": opt.min_select,
                "max_select": opt.max_select,
                "is_active": opt.is_active,
                "values": [
                    {
                        "id": v.id,
                        "value": v.value,
                        "extra_price": v.extra_price,
                        "is_active": v.is_active
                    }
                    for v in opt.values
                ]
            }
            for opt in product.options
        ] if product.options else []

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
            "attributes": attributes_data,
            "options": options_data
        }

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

            return product

        except Exception as e:
            await self.repository.db.rollback()
            print(f"Error creating product: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating product: {str(e)}"
            )
    async def update(self, product_id: int, data: dict):
        async with self.db.begin():
            option_ids = data.pop("options", [])
            variants_data = data.pop("variants", [])
            product = await self.repository.update(product_id, data)
            if not product:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )
            await self.db.refresh(product, ["options", "variants"])
            existing_option_ids = {opt.id for opt in product.options}
            incoming_option_ids = set(option_ids)
            for oid in incoming_option_ids - existing_option_ids:
                await self.product_options_repo.create({
                    "product_id": product.id,
                    "option_id": oid
                })
            for oid in existing_option_ids - incoming_option_ids:
                await self.product_options_repo.delete(product.id, oid)
            existing_variants = {v.id: v for v in product.variants}
            incoming_variant_ids = set()
            for v_data in variants_data:
                attr_value_ids = v_data.pop("attribute_value_ids", [])
                if v_data.get("id"):
                    vid = v_data["id"]
                    incoming_variant_ids.add(vid)
                    variant = await self.variant_repo.update(vid, v_data)
                else:
                    v_data["product_id"] = product.id
                    v_data.setdefault("is_active", True)
                    variant = await self.variant_repo.create(v_data)
                    vid = variant.id
                existing_attr = await self.variant_attribute_value_repo.get_by_variant_id(vid)
                existing_attr_ids = {e.attribute_value_id for e in existing_attr}
                incoming_attr_ids = set(attr_value_ids)
                for aid in incoming_attr_ids - existing_attr_ids:
                    await self.variant_attribute_value_repo.create({
                        "variant_id": vid,
                        "attribute_value_id": aid
                    })
                for aid in existing_attr_ids - incoming_attr_ids:
                    await self.variant_attribute_value_repo.delete(vid, aid)
        await self.repository.db.refresh(product)
        return product

    async def delete(self, product_id: int) -> bool:
        # try:
            deleted = await self.repository.delete(product_id)
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )
            await redis_client.delete("items:products:all")
            return True
        # except HTTPException:
        #     raise
        # except Exception:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Internal server error while deleting product"
        #     )
