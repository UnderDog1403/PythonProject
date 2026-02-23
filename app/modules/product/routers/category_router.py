from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency

from app.modules.product.schemas.category_schema import (
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryResponseSchema
)
from app.modules.product.services.category_service import CategoryService

CategoryRouter = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@CategoryRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model= list[CategoryResponseSchema]
)
async def get_all(
    db:  db_dependency
    # current_user=Depends(require_roles(["admin", "user"]))
):
    category_service = CategoryService(db)

    categories = await category_service.get_all()
    return categories
@CategoryRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryResponseSchema
)
async def create_category(
    payload: CategoryCreateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    category_service = CategoryService(db)

    return await category_service.create_category(
        name=payload.name,
        description=getattr(payload, "description", None)
    )


@CategoryRouter.put(
    "/{category_id}",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponseSchema
)
async def update_category(
    category_id: int,
    payload: CategoryUpdateSchema,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = CategoryService(db)
    update_data = payload.model_dump(exclude_unset=True)
    return await service.update_category(
        category_id=category_id,
        data=update_data
    )
@CategoryRouter.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
    category_id: int,
    db : db_dependency
    # current_user=Depends(require_roles(["admin"]))
):
    service = CategoryService(db)
    await service.delete_category(category_id)
