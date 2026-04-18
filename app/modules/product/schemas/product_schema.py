from pydantic import BaseModel

from app.modules.product.schemas.attribute_schema import AttributeResponseSchema
from app.modules.product.schemas.option_schema import OptionResponseSchema
from app.modules.product.schemas.product_variant_schema import ProductVariantResponseSchema, ProductVariantCreateSchema


class ProductResponseSchema(BaseModel):
    id: int
    name: str
    description: str | None = None
    image_url: str | None = None
    category_id: int
    is_active: bool
    class Config:
        from_attributes = True
class ProductDetailResponseSchema(BaseModel):
    id: int
    name: str
    description: str | None = None
    image_url: str | None = None
    category_id: int
    is_active: bool
    attributes: list[AttributeResponseSchema] | None = None
    variants: list[ProductVariantResponseSchema] | None = None
    options: list[OptionResponseSchema] | None = None
    class Config:
        from_attributes = True
class ProductCreateSchema(BaseModel):
    name: str
    description: str | None = None
    category_id: int
    image_url: str | None = None
    options: list[int] | None = None
    variants: list[ProductVariantCreateSchema]

class ProductUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    category_id: int | None = None
    image_url: str | None = None
    is_active: bool | None = None
