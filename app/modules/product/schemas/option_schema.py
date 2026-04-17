from pydantic import BaseModel

from app.modules.product.schemas.option_value_schema import OptionValueCreateSchema, OptionValueResponseSchema


class OptionResponseSchema(BaseModel):
    id: int
    name: str
    min_select: int
    max_select: int
    is_active: bool
    values: list[OptionValueResponseSchema] = []
    class Config:
        from_attributes = True


class OptionCreateSchema(BaseModel):
    name: str
    min_select: int
    max_select: int
    values: list[OptionValueCreateSchema]

class OptionUpdateSchema(BaseModel):
    name: str | None = None
    min_select: int
    max_select: int
    is_active: bool
