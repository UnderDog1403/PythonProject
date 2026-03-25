from pydantic import BaseModel


class CalculateCartSchema(BaseModel):
    item_keys: list[str]
class RemoveCartItemSchema(BaseModel):
    item_key: str
class CartItemCreateSchema(BaseModel):
    product_variant_id: int
    quantity: int
    option_value_ids: list[int]
class CartItemUpdateSchema(BaseModel):
    item_key: str
    quantity: int

class CartOptionResponse(BaseModel):
    id: int
    value: str
    price: float

class CartItemResponse(BaseModel):
    item_key: str
    variant_id: int
    name: str
    price: float
    quantity: int
    options: list[CartOptionResponse]
    item_total: float

class CartResponse(BaseModel):
    items: list[CartItemResponse]

class CalculateItemResponse(BaseModel):
    item_key: str
    variant_id: int
    name: str
    quantity: int
    item_total: float # Tổng của món đó

class CalculateResponse(BaseModel):
    total_amount: float
    items: list[CalculateItemResponse]
    item_keys: list[str]

