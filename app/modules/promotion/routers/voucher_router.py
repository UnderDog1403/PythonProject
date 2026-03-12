from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency

from app.modules.promotion.schemas.voucher_schema import (
    VoucherCreateSchema,
    VoucherUpdateSchema,
    VoucherResponseSchema
)
from app.modules.promotion.servies.voucher_service import VoucherService

VoucherRouter = APIRouter(
    prefix="/vouchers",
    tags=["Vouchers"]
)

@VoucherRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[VoucherResponseSchema]
)
async def get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    voucher_service = VoucherService(db)

    vouchers = await voucher_service.get_all()
    return vouchers
@VoucherRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=VoucherResponseSchema
)
async def create_voucher(
    payload: VoucherCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    voucher_service = VoucherService(db)

    return await voucher_service.create(
        payload.model_dump(exclude_unset=True)
    )


@VoucherRouter.put(
    "/{voucher_id}",
    status_code=status.HTTP_200_OK,
    response_model=VoucherResponseSchema
)
async def update_voucher(
    voucher_id: int,
    payload: VoucherUpdateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = VoucherService(db)
    update_data = payload.model_dump(exclude_unset=True)
    return await service.update(
        voucher_id=voucher_id,
        data=update_data
    )
@VoucherRouter.delete(
    "/{voucher_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_voucher(
    voucher_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = VoucherService(db)
    await service.delete(voucher_id)
