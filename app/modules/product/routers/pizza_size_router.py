from fastapi import APIRouter

from app.core.dependencies import db_dependency
from app.modules.product.schemas.pizza_size_schema import PizzaSizeCreateSchema, PizzaSizeUpdateSchema, \
    PizzaSizeResponseSchema

from app.modules.product.services.pizza_size_service import PizzaSizeService

PizzaSizeRouter = APIRouter(
    prefix="/pizza-sizes",
    tags=["Pizza Sizes"]
)
@PizzaSizeRouter.get("/",status_code=200, response_model=list[PizzaSizeResponseSchema])
async def get_all_pizza_sizes(
    db: db_dependency
):
    service = PizzaSizeService(db)
    pizza_sizes = await service.get_all_pizza_sizes()
    return pizza_sizes
@PizzaSizeRouter.put("/{pizza_size_id}",status_code=200, response_model=PizzaSizeResponseSchema)
async def update_pizza_size(
    db: db_dependency,
    pizza_size_id: int,
    payload: PizzaSizeUpdateSchema
):
    service = PizzaSizeService(db)
    updated_pizza_size = await service.update_pizza_size(pizza_size_id, payload.model_dump(exclude_unset=True))
    return updated_pizza_size
@PizzaSizeRouter.post("/",status_code=201, response_model=PizzaSizeResponseSchema)
async def create_pizza_size(
    db: db_dependency,
    payload: PizzaSizeCreateSchema
):
    service = PizzaSizeService(db)
    new_pizza_size = await service.create_pizza_size(payload.model_dump(exclude_unset=True))
    return new_pizza_size
@PizzaSizeRouter.delete("/{pizza_size_id}",status_code=204)
async def delete_pizza_size(
    db: db_dependency,
    pizza_size_id: int
):
    service = PizzaSizeService(db)
    await service.delete_pizza_size(pizza_size_id)
    return None