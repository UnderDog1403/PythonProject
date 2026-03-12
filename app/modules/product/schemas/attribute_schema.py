
from pydantic import BaseModel

from app.modules.product.schemas.attribute_value_schema import AttributeValueResponseSchema


class AttributeResponseSchema(BaseModel):
    id: int
    name: str
    values: list[AttributeValueResponseSchema]
    is_active: bool

    class Config:
        from_attributes = True
class AttributeCreateSchema(BaseModel):
    name: str
class AttributeUpdateSchema(BaseModel):
    name: str | None = None
    is_active: bool | None = None