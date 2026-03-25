from datetime import datetime

from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class VoucherResponseSchema(BaseModel):
    id: int
    code: str
    discount_type: str
    discount_value: Decimal
    min_order_value: Decimal
    max_discount_value: Optional[Decimal]
    start_at: datetime
    end_at: datetime
    usage_limit: int
    used_count: int
    is_active: bool
    class Config:
        from_attributes = True
class VoucherCreateSchema(BaseModel):
    code: str
    discount_type: str
    discount_value: Decimal
    min_order_value: Decimal = 0
    max_discount_value: Optional[Decimal] = None
    start_at: datetime
    end_at: datetime
    usage_limit: int = 0
class VoucherUpdateSchema(BaseModel):
    code: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[Decimal] = None
    min_order_value: Optional[Decimal] = None
    max_discount_value: Optional[Decimal] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    usage_limit: Optional[int] = None
    is_active: Optional[bool] = None
