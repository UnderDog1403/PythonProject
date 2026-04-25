from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency

from app.modules.product.schemas.option_schema import (
    OptionCreateSchema,
    OptionUpdateSchema,
    OptionResponseSchema
)
from app.modules.product.services.option_service import OptionService

OptionRouter = APIRouter(
    prefix="/options",
    tags=["Options"]
)
AdminOptionRouter = APIRouter(
    prefix="/admin/options",
    tags=["Admin Options"]
)
@AdminOptionRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[OptionResponseSchema]
)
async def admin_get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    option_service = OptionService(db)

    options = await option_service.admin_get_all()
    return options
@OptionRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[OptionResponseSchema]
)
async def get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    option_service = OptionService(db)

    options = await option_service.get_all()
    return options
@OptionRouter.get(
    "/{option_id}",
    status_code=status.HTTP_200_OK,
    response_model=OptionResponseSchema)
async def get_by_id(
    option_id: int,
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    service = OptionService(db)
    option = await service.get_by_id(option_id)
    return option


@OptionRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=OptionResponseSchema
)
async def create_option(
    payload: OptionCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    option_service = OptionService(db)

    return await option_service.create_option_with_values(
        payload.model_dump(exclude_unset=True)
    )

@OptionRouter.put(
    "/{option_id}",
    status_code=status.HTTP_200_OK,
    response_model=OptionResponseSchema
)
async def update_option(
    option_id: int,
    payload: OptionUpdateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = OptionService(db)
    update_data = payload.model_dump(exclude_unset=True)
    return await service.update_with_option_value(
        option_id=option_id,
        data=update_data
    )
@OptionRouter.delete(
    "/{option_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_option(
    option_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = OptionService(db)
    await service.delete(option_id)
