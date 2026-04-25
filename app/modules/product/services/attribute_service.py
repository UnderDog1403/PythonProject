# modules/attribute/services/attribute_service.py
import json
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.modules.product.models.attribute_model import Attribute
from app.modules.product.models.attribute_value_model import AttributeValue
from app.modules.product.repositories.attribute_repository import AttributeRepository
from app.modules.product.repositories.attribute_value_repository import AttributeValueRepository
from app.modules.product.schemas.attribute_schema import AttributeResponseSchema
from app.modules.product.schemas.attribute_value_schema import AttributeValueResponseSchema


class AttributeService:
    def __init__(self, db: AsyncSession):
        self.repository = AttributeRepository(db)
        self.attribute_value_repo = AttributeValueRepository(db)
        self.db = db
    async def get_all(self)-> list[AttributeResponseSchema]:

        # try:
        attributes = await self.repository.get_all()
        result = []
        for a in attributes:
            result.append(
                AttributeResponseSchema(
                    id=a.id,
                    name=a.name,
                    values=[
                        AttributeValueResponseSchema(
                            id=v.id,
                            value=v.value,
                            attribute_id=v.attribute_id,
                            is_active=v.is_active
                        ) for v in a.values
                    ],
                    is_active=a.is_active
                )
            )
        return result
        # except Exception:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Internal server error while retrieving attributes"
        #     )
    async def admin_get_all(self)-> list[AttributeResponseSchema]:
        attributes = await self.repository.admin_get_all()
        return attributes
    async def get_by_id(self, attribute_id: int) -> Optional[AttributeResponseSchema]:
        try:
            attribute = await self.repository.get_by_id(attribute_id)
            if not attribute:
                raise HTTPException(
                    status_code=404,
                    detail="Attribute not found"
                )
            return attribute
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while retrieving attribute"
            )
    # async def get_attributes_paginated(
    #     self,
    #     page: int = 1,
    #     limit: int = 10,
    #     order_by: str = "id",
    #     descending: bool = False,
    # ) -> Tuple[List[Attribute], int, int]:
    #
    #     # validate inputs
    #     if page < 1 or limit < 1:
    #         raise HTTPException(
    #             status_code=400,
    #             detail="`page` and `limit` must be positive integers"
    #         )
    #
    #     try:
    #         items, total, total_pages = await self.repository.get_attributes_paginated(
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
    #             detail="Internal server error while retrieving attributes"
    #         )

    async def create(self, data: dict):
        values_data = data.pop("values", [])
        db_attribute_values = [
            AttributeValue(**val_data)
            for val_data in values_data
        ]
        db_attribute = Attribute(**data, values=db_attribute_values)
        try:
            # 4. GỌI REPOSITORY (Repo của bạn đã có sẵn self.db.add và flush)
            created_attribute = await self.repository.create(db_attribute)

            # 5. CHỐT GIAO DỊCH
            await self.db.commit()
            await self.db.refresh(created_attribute, ["values"])
            return created_attribute

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Đã tồn tại dữ liệu."
            )
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Lỗi hệ thống không xác định: {str(e)}"
            )
    async def update_with_attribute_value(self, attribute_id: int, data: dict):
        async with self.db.begin():
            values_data = data.pop("values",[])
            attribute = await self.repository.update(attribute_id, data)
            if not attribute:
                raise HTTPException(
                    status_code=404,
                    detail=f"Attribute not found"
                )
            for val_data in values_data:
                val_data["attribute_id"] = attribute_id
                if "id" in val_data:
                    await self.attribute_value_repo.update(
                        val_data["id"],
                        val_data
                    )
                else:
                    await self.attribute_value_repo.create(val_data)
        await self.db.refresh(attribute, ["values"])
        return attribute
    async def delete(self, attribute_id: int) -> bool:
        try:
            deleted = await self.repository.delete(attribute_id)
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="Attribute not found"
                )
            return True
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting attribute"
            )
