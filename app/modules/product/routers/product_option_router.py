from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency

from app.modules.product.schemas.product_option_schema import (
    ProductOptionCreateSchema,
    ProductOptionResponseSchema
)
from app.modules.product.services.product_option_service import ProductOptionService

ProductOptionRouter = APIRouter(
    prefix="/product_options",
    tags=["ProductOptions"]
)

@ProductOptionRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[ProductOptionResponseSchema]
)
async def get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    product_option_service = ProductOptionService(db)

    product_options = await product_option_service.get_all()
    return product_options
@ProductOptionRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductOptionResponseSchema
)
async def create_product_option(
    payload: ProductOptionCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    product_option_service = ProductOptionService(db)

    return await product_option_service.create(
        payload.model_dump(exclude_unset=True)
    )



@ProductOptionRouter.delete(
    "/{product_option_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product_option(
    product_option_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = ProductOptionService(db)
    await service.delete(product_option_id)
