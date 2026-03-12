from pydantic import BaseModel


class ProductOptionResponseSchema(BaseModel):
    product_id: int
    option_id: int

    class Config:
        from_attributes = True
class ProductOptionCreateSchema(BaseModel):
    product_id: int
    option_id: int