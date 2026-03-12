from pydantic import BaseModel


class ProductVariantResponseSchema(BaseModel):
    id: int
    price: int
    product_id: int
    attribute_value_ids: list[int]
    is_active: bool
    class Config:
        from_attributes = True
class ProductVariantCreateSchema(BaseModel):
    price: int
    product_id: int
class ProductVariantUpdateSchema(BaseModel):
    price: int | None = None
    product_id: int | None = None
    is_active: bool | None = None
