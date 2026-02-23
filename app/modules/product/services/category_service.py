# modules/product/services/category_service.py
import json
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.modules.product.models.category_model import Category
from app.modules.product.repositories.category_repository import CategoryRepository
from app.modules.product.schemas.category_schema import CategoryResponseSchema, CategoryListResponseSchema


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.repository = CategoryRepository(db)
    async def get_all(self)-> list[CategoryResponseSchema]:
        cached_item = await redis_client.get(f"items:categories:all")
        if cached_item:
            data = json.loads(cached_item)
            return TypeAdapter(List[CategoryResponseSchema]).validate_python(data)
        # try:
        categories = await self.repository.get_all()
        categories_data = TypeAdapter(
            list[CategoryResponseSchema]
        ).dump_python(categories)
        await redis_client.set(
                f"items:categories:all",
                json.dumps(categories_data),
                ex=3600  # cache for 1 hour
            )
        return categories_data
        # except Exception:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Internal server error while retrieving categories"
        #     )
    # async def get_categories_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False,
    # ) -> Tuple[List[Category], int, int]:
    #
    #     # validate inputs
    #     if page < 1 or limit < 1:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="`page` and `limit` must be positive integers"
    #         )
    #
    #     try:
    #         items, total, total_pages = await self.repository.get_categories_paginated(
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
    #             detail="Internal server error while retrieving categories"
    #         )

    async def create_category(
        self,
        name: str,
        description: Optional[str] = None
    ) -> Category:

        if not name or not isinstance(name, str) or not name.strip():
            raise HTTPException(
                status_code=400,
                detail="`name` is required and must be a non-empty string"
            )

        try:
            category = await self.repository.create_category(
                name=name.strip(),
                description=description
            )
            await redis_client.delete("items:categories:all")
            return category
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while creating category"
            )

    async def update_category(
        self,
        category_id: int,
        data: Dict[str, Any]
    ) -> Category:

        if not isinstance(category_id, int) or category_id < 1:
            raise HTTPException(
                status_code=400,
                detail="`category_id` must be a positive integer"
            )

        if not isinstance(data, dict) or not data:
            raise HTTPException(
                status_code=400,
                detail="`data` must be a non-empty object with fields to update"
            )

        # prevent updating id
        data = {k: v for k, v in data.items() if k != "id"}

        try:
            updated = await self.repository.update_category(category_id, data)
            if not updated:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found"
                )
            await redis_client.delete("items:categories:all")
            return updated
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while updating category"
            )
    async def delete_category(self, category_id: int) -> bool:

        if not isinstance(category_id, int) or category_id < 1:
            raise HTTPException(
                status_code=400,
                detail="`category_id` must be a positive integer"
            )

        try:
            deleted = await self.repository.delete_category(category_id)
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="Category not found"
                )
            await redis_client.delete("items:categories:all")
            return True
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting category"
            )
