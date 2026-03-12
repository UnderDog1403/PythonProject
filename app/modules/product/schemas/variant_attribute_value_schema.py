from pydantic import BaseModel


class VariantAttributeValueResponseSchema(BaseModel):
    variant_id: int
    attribute_value_id: int

    class Config:
        from_attributes = True
class VariantAttributeValueCreateSchema(BaseModel):
    variant_id: int
    attribute_value_id: int