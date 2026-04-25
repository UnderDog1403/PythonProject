from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency
from app.core.security import require_roles

from app.modules.product.schemas.product_schema import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductResponseSchema, ProductDetailResponseSchema
)
from app.modules.product.services.product_service import ProductService

ProductRouter = APIRouter(
    prefix="/products",
    tags=["Products"]
)
AdminProductRouter = APIRouter(
    prefix="/admin/products",
    tags=["Admin Products"]
)
@AdminProductRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[ProductResponseSchema]
)
async def admin_get_all(
    db:  db_dependency,
    current_user=Depends(require_roles(["admin"]))
):
    product_service = ProductService(db)

    products = await product_service.get_all()
    return products

@ProductRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[ProductResponseSchema]
)
async def get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    product_service = ProductService(db)

    products = await product_service.get_all()
    return products
@ProductRouter.get(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductDetailResponseSchema)
async def get_by_id(
    product_id: int,
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    service = ProductService(db)
    product = await service.get_by_id(product_id)
    return product


@ProductRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProductResponseSchema
)
async def create_product(
    payload: ProductCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    product_service = ProductService(db)

    return await product_service.create(
        payload.model_dump(exclude_unset=True)
    )


@ProductRouter.put(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=ProductResponseSchema
)
async def update_product(
    product_id: int,
    payload: ProductUpdateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = ProductService(db)
    update_data = payload.model_dump(exclude_unset=True)
    return await service.update(
        product_id=product_id,
        data=update_data
    )
@ProductRouter.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
    product_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = ProductService(db)
    await service.delete(product_id)
