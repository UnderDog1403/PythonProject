
from pydantic import BaseModel
class AttributeValueResponseSchema(BaseModel):
    id: int
    value: str
    is_active: bool

    class Config:
        from_attributes = True
class AttributeValueCreateSchema(BaseModel):
    value: str
class AttributeValueUpdateSchema(BaseModel):
    attribute_id : int | None = None
    value: str | None = None
    is_active: bool | None = None