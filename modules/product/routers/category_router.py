
from fastapi import APIRouter
from fastapi.params import Depends
from starlette import status

from core.dependencies import db_dependency
from core.security import require_roles

from modules.product.schemas.category_schema import CategoryListResponseSchema, CategoryCreateSchema, \
    CategoryUpdateSchema, CategoryResponseSchema
from modules.product.services.category_service import CategoryService

CategoryRouter= APIRouter(
    prefix="/categories",
    tags=["Categories"]
)
@CategoryRouter.get("/",status_code=status.HTTP_200_OK,response_model=CategoryListResponseSchema)
def get_categories_paginated(
        db: db_dependency,
        page: int = 1,
        limit: int = 10,
        current_user=Depends(require_roles(["admin"]))
):
    category_service = CategoryService(db)
    categories, total, total_page = category_service.get_categories_paginated(page, limit)
    return CategoryListResponseSchema(
        categories=categories,
        total=total,
        total_pages=total_page,
        page=page,
        limit=limit
    )
@CategoryRouter.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema,
    db: db_dependency,
    current_user=Depends(require_roles(["admin"]))
):
    category_service = CategoryService(db)
    return category_service.create_category(name=payload.name, description=getattr(payload, "description", None))


@CategoryRouter.put("/{category_id}", status_code=200, response_model=CategoryResponseSchema)
def update_category(
    category_id: int,
    payload: CategoryUpdateSchema,
    db: db_dependency,
    current_user=Depends(require_roles(["admin"]))
):
    service = CategoryService(db)
    update_data = payload.model_dump(exclude_unset=True)
    return service.update_category(category_id=category_id, data=update_data)
