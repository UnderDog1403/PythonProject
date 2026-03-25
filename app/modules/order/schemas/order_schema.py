from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.modules.order.models.order_model import DeliveryType, PaymentMethod


class OrderCreateSchema(BaseModel):
    customer_name: str
    customer_phone: str
    delivery_type: DeliveryType
    delivery_address: Optional[str] = None
    pickup_time: Optional[datetime] = None
    payment_method: PaymentMethod
    voucher_code: Optional[str] = None
class CheckoutRequest(BaseModel):
    selected_items: list[str]
    checkout_info: OrderCreateSchema
class OrderStatusUpdate(BaseModel):
    status: str