from pydantic import BaseModel


class OptionValueResponseSchema(BaseModel):
    id: int
    value: str
    extra_price: int
    is_active: bool
    class Config:
        from_attributes = True
class OptionValueCreateSchema(BaseModel):
    value: str
    extra_price: int

class OptionValueUpdateSchema(BaseModel):
    id: int | None = None
    value: str | None = None
    extra_price: int | None = None
    is_active: bool | None = None
