from pydantic import BaseModel

class CalculateCartSchema(BaseModel):
    variant_ids: list[int]
class CartItemCreateSchema(BaseModel):
    product_variant_id: int
    quantity: int