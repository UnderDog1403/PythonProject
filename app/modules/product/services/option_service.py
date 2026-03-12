# modules/option/services/option_service.py
import json
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.modules.product.models.option_model import Option
from app.modules.product.repositories.option_repository import OptionRepository
from app.modules.product.schemas.option_schema import OptionResponseSchema


class OptionService:
    def __init__(self, db: AsyncSession):
        self.repository = OptionRepository(db)
    async def get_all(self)-> list[OptionResponseSchema]:

        # try:
        options = await self.repository.get_all()
        return options
        # except Exception:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Internal server error while retrieving options"
        #     )
    # async def get_options_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False,
    # ) -> Tuple[List[Option], int, int]:
    #
    #     # validate inputs
    #     if page < 1 or limit < 1:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="`page` and `limit` must be positive integers"
    #         )
    #
    #     try:
    #         items, total, total_pages = await self.repository.get_options_paginated(
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
    #             detail="Internal server error while retrieving options"
    #         )

    async def create(self, data: dict):
        try:
            option =await self.repository.create(data)
            return option
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating pizza: {str(e)}"
            )
    async def update(self, option_id: int, data: dict):
        try:
            option = await self.repository.update(option_id, data)
            if not option:
                raise HTTPException(
                    status_code=404,
                    detail=f"Option not found"
                )
            return option
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while updating pizza: {str(e)}"
            )
    async def delete(self, option_id: int) -> bool:
        try:
            deleted = await self.repository.delete(option_id)
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="Option not found"
                )
            return True
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting option"
            )
