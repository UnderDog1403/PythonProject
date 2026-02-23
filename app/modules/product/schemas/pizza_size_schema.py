from pydantic import BaseModel

class PizzaSizeResponseSchema(BaseModel):
    id: int
    name: str
    coefficient_price: float

    class Config:
        from_attributes = True
class PizzaSizeCreateSchema(BaseModel):
    name: str
    coefficient_price: float
class PizzaSizeUpdateSchema(BaseModel):
    name: str | None = None
    coefficient_price: float | None = None
    is_actived: bool | None = None