# modules/voucher/services/voucher_service.py
import json
from typing import Tuple, List, Dict, Any, Optional
from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.redis import redis_client
from app.modules.promotion.models.voucher_model import Voucher
from app.modules.promotion.repositories.voucher_repository import VoucherRepository
from app.modules.promotion.schemas.voucher_schema import VoucherResponseSchema


class VoucherService:
    def __init__(self, db: AsyncSession):
        self.repository = VoucherRepository(db)
    async def get_all(self)-> list[VoucherResponseSchema]:

        # try:
        vouchers = await self.repository.get_all()
        return vouchers
        # except Exception:
        #     raise HTTPException(
        #         status_code=500,
        #         detail="Internal server error while retrieving vouchers"
        #     )

    async def create(self, data: dict):
        try:
            voucher =await self.repository.create(data)
            return voucher
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while creating pizza: {str(e)}"
            )
    async def update(self, voucher_id: int, data: dict):
        try:
            voucher = await self.repository.update(voucher_id, data)
            if not voucher:
                raise HTTPException(
                    status_code=404,
                    detail=f"Voucher not found"
                )
            return voucher
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error while updating pizza: {str(e)}"
            )
    async def delete(self, voucher_id: int) -> bool:
        try:
            deleted = await self.repository.delete(voucher_id)
            if not deleted:
                raise HTTPException(
                    status_code=404,
                    detail="Voucher not found"
                )
            return True
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="Internal server error while deleting voucher"
            )
