from fastapi import APIRouter, status

from app.core.dependencies import db_dependency
from app.modules.product.schemas.pizza_schema import PizzaListResponseSchema, PizzaResponseSchema, PizzaCreateSchema, \
    PizzaUpdateSchema
from app.modules.product.services.pizza_service import PizzaService

PizzaRouter= APIRouter(
    prefix="/pizzas",
    tags=["Pizzas"]
)
@PizzaRouter.get("/",status_code=status.HTTP_200_OK, response_model=PizzaListResponseSchema)
async def get_pizzas_paginated(
    db: db_dependency,
    page: int = 1,
    limit: int = 10,
    order_by: str = "id",
    descending: bool = False
):
    service = PizzaService(db)
    pizzas, total, total_pages = await service.get_pizzas_paginated(
        page=page,
        limit=limit,
        order_by=order_by,
        descending=descending
    )
    return PizzaListResponseSchema(
        pizzas=pizzas,
        total=total,
        total_pages=total_pages,
        page=page,
        limit=limit
    )
@PizzaRouter.post("/",status_code=status.HTTP_201_CREATED, response_model=PizzaResponseSchema)
async def create_pizza(
    db: db_dependency,
    payload: PizzaCreateSchema
):
    service = PizzaService(db)
    new_pizza = await service.create_pizza(payload.model_dump(exclude_unset=True))
    return new_pizza
@PizzaRouter.get("/{pizza_id}",status_code=status.HTTP_200_OK, response_model=PizzaResponseSchema)
async def get_pizza_by_id(
    db: db_dependency,
    pizza_id: int
):
    service = PizzaService(db)
    pizza = await service.get_pizza_by_id(pizza_id)
    return pizza
@PizzaRouter.put("/{pizza_id}",status_code=status.HTTP_200_OK, response_model=PizzaResponseSchema)
async def update_pizza(
    db: db_dependency,
    pizza_id: int,
    payload: PizzaUpdateSchema
):
    service = PizzaService(db)
    updated_pizza = await service.update_pizza(pizza_id, payload.model_dump(exclude_unset=True))
    return updated_pizza
@PizzaRouter.delete("/{pizza_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_pizza(
    db: db_dependency,
    pizza_id: int
):
    service = PizzaService(db)
    await service.delete_pizza(pizza_id)
    return None