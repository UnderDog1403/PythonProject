from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency

from app.modules.product.schemas.attribute_schema import (
    AttributeCreateSchema,
    AttributeUpdateSchema,
    AttributeResponseSchema
)
from app.modules.product.services.attribute_service import AttributeService

AttributeRouter = APIRouter(
    prefix="/attributes",
    tags=["Attributes"]
)
AdminAttributeRouter = APIRouter(
    prefix="/admin/attributes",
    tags=["Admin Attributes"]
)
@AdminAttributeRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[AttributeResponseSchema]
)
async def admin_get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    attribute_service = AttributeService(db)

    attributes = await attribute_service.admin_get_all()
    return attributes
@AttributeRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[AttributeResponseSchema]
)
async def get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    attribute_service = AttributeService(db)

    attributes = await attribute_service.get_all()
    return attributes
@AttributeRouter.get(
    "/{attribute_id}",
    status_code=status.HTTP_200_OK,
    response_model=AttributeResponseSchema)
async def get_by_id(
    attribute_id: int,
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    service = AttributeService(db)
    attribute = await service.get_by_id(attribute_id)
    return attribute
@AttributeRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AttributeResponseSchema
)
async def create_attribute(
    payload: AttributeCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    attribute_service = AttributeService(db)

    return await attribute_service.create(
        payload.model_dump(exclude_unset=True)
    )


@AttributeRouter.put(
    "/{attribute_id}",
    status_code=status.HTTP_200_OK,
    response_model=AttributeResponseSchema
)
async def update_attribute(
    attribute_id: int,
    payload: AttributeUpdateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = AttributeService(db)
    update_data = payload.model_dump(exclude_unset=True)
    return await service.update_with_attribute_value(
        attribute_id,update_data
    )
@AttributeRouter.delete(
    "/{attribute_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_attribute(
    attribute_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = AttributeService(db)
    await service.delete(attribute_id)
