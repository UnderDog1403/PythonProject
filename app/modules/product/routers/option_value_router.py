from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency

from app.modules.product.schemas.option_value_schema import (
    OptionValueCreateSchema,
    OptionValueUpdateSchema,
    OptionValueResponseSchema
)
from app.modules.product.services.option_value_service import OptionValueService

OptionValueRouter = APIRouter(
    prefix="/option_values",
    tags=["OptionValues"]
)

@OptionValueRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[OptionValueResponseSchema]
)
async def get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    option_value_service = OptionValueService(db)

    option_values = await option_value_service.get_all()
    return option_values
@OptionValueRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=OptionValueResponseSchema
)
async def create_option_value(
    payload: OptionValueCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    option_value_service = OptionValueService(db)

    return await option_value_service.create(
        payload.model_dump(exclude_unset=True)
    )


@OptionValueRouter.put(
    "/{option_value_id}",
    status_code=status.HTTP_200_OK,
    response_model=OptionValueResponseSchema
)
async def update_option_value(
    option_value_id: int,
    payload: OptionValueUpdateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = OptionValueService(db)
    update_data = payload.model_dump(exclude_unset=True)
    return await service.update(
        option_value_id=option_value_id,
        data=update_data
    )
@OptionValueRouter.delete(
    "/{option_value_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_option_value(
    option_value_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = OptionValueService(db)
    await service.delete(option_value_id)
