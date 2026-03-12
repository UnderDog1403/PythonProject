from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency

from app.modules.product.schemas.variant_attribute_value_schema import (
    VariantAttributeValueCreateSchema,
    VariantAttributeValueResponseSchema
)
from app.modules.product.services.variant_attribute_value import VariantAttributeValueService

VariantAttributeValueRouter = APIRouter(
    prefix="/variant_attribute_values",
    tags=["VariantAttributeValues"]
)

@VariantAttributeValueRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[VariantAttributeValueResponseSchema]
)
async def get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    variant_attribute_value_service = VariantAttributeValueService(db)

    variant_attribute_values = await variant_attribute_value_service.get_all()
    return variant_attribute_values
@VariantAttributeValueRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=VariantAttributeValueResponseSchema
)
async def create_variant_attribute_value(
    payload: VariantAttributeValueCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    variant_attribute_value_service = VariantAttributeValueService(db)

    return await variant_attribute_value_service.create(
        payload.model_dump(exclude_unset=True)
    )



@VariantAttributeValueRouter.delete(
    "/{variant_attribute_value_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_variant_attribute_value(
    variant_attribute_value_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = VariantAttributeValueService(db)
    await service.delete(variant_attribute_value_id)
