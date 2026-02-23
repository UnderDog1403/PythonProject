from fastapi import APIRouter

from app.core.dependencies import db_dependency
from app.modules.product.schemas.pizza_topping_schema import PizzaToppingUpdateSchema, PizzaToppingCreateSchema, \
    PizzaToppingResponseSchema
from app.modules.product.services.pizza_topping_service import PizzaToppingService

PizzaToppingRouter = APIRouter(
    prefix="/pizza-toppings",
    tags=["Pizza Toppings"]
)
@PizzaToppingRouter.get("/",status_code=200,response_model=list[PizzaToppingResponseSchema])
async def get_all(
        db: db_dependency
):
    service = PizzaToppingService(db)
    toppings = await service.get_all_pizza_toppings()
    return toppings
@PizzaToppingRouter.put("/{pizza_topping_id}",status_code=200,response_model=PizzaToppingResponseSchema)
async def update_pizza_topping(
    db: db_dependency,
    pizza_topping_id: int,
    payload: PizzaToppingUpdateSchema
):
    service = PizzaToppingService(db)
    updated_pizza_topping = await service.update_pizza_topping(pizza_topping_id, payload.model_dump(exclude_unset=True))
    return updated_pizza_topping
@PizzaToppingRouter.post("/",status_code=201, response_model=PizzaToppingResponseSchema)
async def create_pizza_topping(
    db: db_dependency,
    payload: PizzaToppingCreateSchema
):
    service = PizzaToppingService(db)
    new_pizza_topping = await service.create_pizza_topping(payload.model_dump(exclude_unset=True))
    return new_pizza_topping
@PizzaToppingRouter.delete("/{pizza_topping_id}",status_code=204)
async def delete_pizza_topping(
    db: db_dependency,
    pizza_topping_id: int
):
    service = PizzaToppingService(db)
    await service.delete_pizza_topping(pizza_topping_id)
    return None
    