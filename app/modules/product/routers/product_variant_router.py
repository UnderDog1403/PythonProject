from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency

from app.modules.product.schemas.product_variant_schema import (
    ProductVariantCreateSchema,
    ProductVariantUpdateSchema,
    ProductVariantResponseSchema
)
from app.modules.product.services.product_variant_service import ProductVariantService

ProductVariantRouter = APIRouter(
    prefix="/product_variants",
    tags=["ProductVariants"]
)

@ProductVariantRouter.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model= list[ProductVariantResponseSchema]
)
async def get_all_by_product_id(
    db:  db_dependency,
    product_id : int,
    # current_user=Depends(require_roles(["admin", "user"]))
):
    product_variant_service = ProductVariantService(db)

    product_variants = await product_variant_service.get_all_by_product_id(product_id)
    return product_variants
@ProductVariantRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductVariantResponseSchema
)
async def create_product_variant(
    payload: ProductVariantCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    product_variant_service = ProductVariantService(db)

    return await product_variant_service.create(
        payload.model_dump(exclude_unset=True)
    )


@ProductVariantRouter.put(
    "/{product_variant_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductVariantResponseSchema
)
async def update_product_variant(
    product_variant_id: int,
    payload: ProductVariantUpdateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = ProductVariantService(db)
    update_data = payload.model_dump(exclude_unset=True)
    return await service.update(
        product_variant_id=product_variant_id,
        data=update_data
    )
@ProductVariantRouter.delete(
    "/{product_variant_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product_variant(
    product_variant_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = ProductVariantService(db)
    await service.delete(product_variant_id)
