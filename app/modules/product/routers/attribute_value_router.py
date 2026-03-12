from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency

from app.modules.product.schemas.attribute_value_schema import (
    AttributeValueCreateSchema,
    AttributeValueUpdateSchema,
    AttributeValueResponseSchema
)
from app.modules.product.services.attribute_value_service import AttributeValueService

AttributeValueRouter = APIRouter(
    prefix="/attribute_values",
    tags=["AttributeValues"]
)

@AttributeValueRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[AttributeValueResponseSchema]
)
async def get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    attribute_value_service = AttributeValueService(db)

    attribute_values = await attribute_value_service.get_all()
    return attribute_values
@AttributeValueRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=AttributeValueResponseSchema
)
async def create_attribute_value(
    payload: AttributeValueCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    attribute_value_service = AttributeValueService(db)

    return await attribute_value_service.create(
        payload.model_dump(exclude_unset=True)
    )


@AttributeValueRouter.put(
    "/{attribute_value_id}",
    status_code=status.HTTP_200_OK,
    response_model=AttributeValueResponseSchema
)
async def update_attribute_value(
    attribute_value_id: int,
    payload: AttributeValueUpdateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = AttributeValueService(db)
    update_data = payload.model_dump(exclude_unset=True)
    return await service.update(
        attribute_value_id=attribute_value_id,
        data=update_data
    )
@AttributeValueRouter.delete(
    "/{attribute_value_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_attribute_value(
    attribute_value_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = AttributeValueService(db)
    await service.delete(attribute_value_id)
