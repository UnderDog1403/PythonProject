
from pydantic import BaseModel

from app.modules.product.schemas.attribute_value_schema import AttributeValueResponseSchema, AttributeValueCreateSchema


class AttributeResponseSchema(BaseModel):
    id: int
    name: str
    values: list[AttributeValueResponseSchema]
    is_active: bool

    class Config:
        from_attributes = True
class AttributeCreateSchema(BaseModel):
    name: str
    values: list[AttributeValueCreateSchema]
class AttributeUpdateSchema(BaseModel):
    name: str | None = None
    is_active: bool | None = None