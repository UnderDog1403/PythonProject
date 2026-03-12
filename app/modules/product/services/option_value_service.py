# modules/option_value/services/option_value_service.py
import json
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.modules.product.models.option_value_model import OptionValue
from app.modules.product.repositories.option_value_repository import OptionValueRepository
from app.modules.product.schemas.option_value_schema import OptionValueResponseSchema


class OptionValueService:
    def __init__(self, db: AsyncSession):
        self.repository = OptionValueRepository(db)
    async def get_all(self)-> list[OptionValueResponseSchema]:

        # try:
        option_values = await self.repository.get_all()
        return option_values
        # except Exception:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Internal server error while retrieving option_values"
        #     )
    # async def get_option_values_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False,
    # ) -> Tuple[List[OptionValue], int, int]:
    #
    #     # validate inputs
    #     if page < 1 or limit < 1:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="`page` and `limit` must be positive integers"
    #         )
    #
    #     try:
    #         items, total, total_pages = await self.repository.get_option_values_paginated(
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
    #             detail="Internal server error while retrieving option_values"
    #         )

    async def create(self, data: dict):
        try:
            option_value =await self.repository.create(data)
            return option_value
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating pizza: {str(e)}"
            )
    async def update(self, option_value_id: int, data: dict):
        try:
            option_value = await self.repository.update(option_value_id, data)
            if not option_value:
                raise HTTPException(
                    status_code=404,
                    detail=f"OptionValue not found"
                )
            return option_value
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while updating pizza: {str(e)}"
            )
    async def delete(self, option_value_id: int) -> bool:
        try:
            deleted = await self.repository.delete(option_value_id)
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="OptionValue not found"
                )
            return True
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting option_value"
            )
