from pydantic import BaseModel


class PizzaToppingResponseSchema(BaseModel):
    id: int
    name: str
    price: float
    is_actived: bool

    class Config:
        from_attributes = True
class PizzaToppingCreateSchema(BaseModel):
    name: str
    price: float
class PizzaToppingUpdateSchema(BaseModel):
    name: str | None = None
    price: float | None = None
    is_actived: bool | None = None