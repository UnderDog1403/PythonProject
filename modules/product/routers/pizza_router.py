from fastapi import APIRouter, Depends, status

from core.dependencies import db_dependency
from core.security import require_roles
from modules.product.schemas.pizza_schema import PizzaListResponseSchema, PizzaResponseSchema, PizzaCreateSchema
from modules.product.services.pizza_service import PizzaService

PizzaRouter= APIRouter(
    prefix="/pizzas",
    tags=["Pizzas"]
)
@PizzaRouter.get("/",status_code=status.HTTP_200_OK,response_model=PizzaListResponseSchema)
def get_pizzas_paginated(
        db: db_dependency,
        page: int = 1,
        limit: int = 10,
        # current_user=Depends(require_roles(["admin", "user"]))
):
    pizza_service = PizzaService(db)
    pizzas, total, total_pages = pizza_service.get_active_pizzas_paginated(
        page=page, limit=limit
    )
    return PizzaListResponseSchema(
        pizzas = pizzas,
        total=total,
        total_pages=total_pages,
        page=page,
        limit=limit
    )
@PizzaRouter.get("/{pizza_id}",status_code=status.HTTP_200_OK,response_model=PizzaResponseSchema)
def get_pizza_by_id(
        db: db_dependency,
        pizza_id: int,
        # current_user=Depends(require_roles(["admin", "user"]))
):
    pizza_service = PizzaService(db)
    pizza = pizza_service.get_pizza_by_id(pizza_id)
    return PizzaResponseSchema(
        id=pizza.id,
        name=pizza.name,
        base_price=pizza.base_price,
        image=pizza.image,
        is_actived=pizza.is_actived
    )

@PizzaRouter.post("/",status_code=status.HTTP_201_CREATED)
def create_pizza(
        db: db_dependency,
        payload: PizzaCreateSchema,
        # current_user=Depends(require_roles(["admin"])),

):
    pizza_service = PizzaService(db)
    new_pizza = pizza_service.create_pizza(payload.model_dump(exclude_unset=True))
    return new_pizza
@PizzaRouter.put("/{pizza_id}",status_code=status.HTTP_200_OK, response_model=PizzaResponseSchema)
def update_pizza(
        db: db_dependency,
        pizza_id: int,
        payload: PizzaCreateSchema,
        # current_user=Depends(require_roles(["admin"]))
):
    pizza_service = PizzaService(db)
    updated_pizza = pizza_service.update_pizza(pizza_id, payload.model_dump(exclude_unset=True))
    return updated_pizza
@PizzaRouter.delete("/{pizza_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_pizza(
        db: db_dependency,
        pizza_id: int,
        # current_user=Depends(require_roles(["admin"]))
):
    pizza_service = PizzaService(db)
    return pizza_service.delete_pizza(pizza_id)
@PizzaRouter.get("/search/",status_code=status.HTTP_200_OK,response_model=PizzaListResponseSchema)
def search_active_pizzas_paginated(
        db: db_dependency,
        keyword: str = "",
        page: int = 1,
        limit: int = 10,
        # current_user=Depends(require_roles(["admin", "user"]))
):
    pizza_service = PizzaService(db)
    pizzas, total, total_pages = pizza_service.search_active_pizzas_paginated(
        keyword=keyword,
        page=page,
        limit=limit
    )
    return PizzaListResponseSchema(
        pizzas=pizzas,
        total=total,
        total_pages=total_pages,
        page=page,
        limit=limit
    )

