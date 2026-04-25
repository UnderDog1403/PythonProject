# modules/option/services/option_service.py
import json
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.modules.product.models.option_model import Option
from app.modules.product.models.option_value_model import OptionValue
from app.modules.product.repositories.option_repository import OptionRepository
from app.modules.product.repositories.option_value_repository import OptionValueRepository
from app.modules.product.schemas.option_schema import OptionResponseSchema


class OptionService:
    def __init__(self, db: AsyncSession):
        self.repository = OptionRepository(db)
        self.option_value_repo = OptionValueRepository(db)
        self.db = db
    async def get_all(self)-> list[OptionResponseSchema]:
        options = await self.repository.get_all()
        return options
    async def admin_get_all(self)-> list[OptionResponseSchema]:
        options = await self.repository.admin_get_all()
        return options
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
    async def get_by_id(self, option_id: int) -> Optional[Option]:
        try:
            option = await self.repository.get_by_id(option_id)
            if not option:
                raise HTTPException(
                    status_code=404,
                    detail="Option not found"
                )
            return option
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving option"
            )


    async def create_option_with_values(self, data: dict):
        values_data = data.pop("values", [])
        db_option_values = [
            OptionValue(**val_data)
            for val_data in values_data
        ]
        db_option = Option(**data, values=db_option_values)
        try:
            # 4. GỌI REPOSITORY (Repo của bạn đã có sẵn self.db.add và flush)
            created_option = await self.repository.create(db_option)

            # 5. CHỐT GIAO DỊCH
            await self.db.commit()
            await self.db.refresh(created_option, ["values"])
            return created_option

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Tên Option hoặc giá trị OptionValue đã tồn tại."
            )
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Lỗi hệ thống không xác định: {str(e)}"
            )

    async def update_with_option_value(self, option_id: int, data: dict):
        async with self.db.begin():
            values_data = data.pop("values", [])
            option = await self.repository.update(option_id, data)
            if not option:
                raise HTTPException(
                    status_code=404,
                    detail=f"Attribute not found"
                )
            for val_data in values_data:
                val_data["option_id"] = option_id
                if "id" in val_data:
                    await self.option_value_repo.update(
                        val_data["id"],
                        val_data
                    )
                else:
                    await self.option_value_repo.create(val_data)
        await self.db.refresh(option, ["values"])
        return option
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
