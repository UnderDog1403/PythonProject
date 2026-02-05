from pydantic import BaseModel
from typing import List

class PizzaResponseSchema(BaseModel):
    id : int
    name : str
    base_price : float
    image : str | None = None
    is_actived : bool
    class Config:
        from_attributes = True
class PizzaListResponseSchema(BaseModel):
    pizzas : List[PizzaResponseSchema]
    total : int
    page : int
    limit : int
    total_pages : int
class PizzaCreateSchema(BaseModel):
    name : str
    base_price : float
    image : str | None = None
    is_actived : bool = True
class PizzaUpdateSchema(BaseModel):
    name : str | None = None
    base_price : float | None = None
    image : str | None = None
    is_actived : bool | None = None