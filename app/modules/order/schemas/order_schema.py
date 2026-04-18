from decimal import Decimal

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.modules.order.models.order_model import OrderType, PaymentMethod, PaymentStatus, OrderStatus


class OrderResponseSchema(BaseModel):
    id: int
    total_amount: Decimal
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True


class OrderCreateSchema(BaseModel):
    customer_name: str
    customer_phone: str
    order_type: OrderType
    delivery_address: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    payment_method: PaymentMethod
    voucher_code: Optional[str] = None
class CheckoutRequest(BaseModel):
    selected_items: list[str]
    checkout_info: OrderCreateSchema
class OrderStatusUpdate(BaseModel):
    status: OrderStatus
class OrderItemOptionResponseSchema(BaseModel):
    option_value_name: str
    extra_price: float

    class Config:
        from_attributes = True
class OrderItemResponseSchema(BaseModel):
    product_name: str
    quantity: int
    price: Decimal
    note: Optional[str] = None
    options: List[OrderItemOptionResponseSchema] = []

    class Config:
        from_attributes = True
class OrderDetailResponseSchema(BaseModel):
    id: int

    user_id: str
    voucher_id: Optional[int]

    subtotal: Decimal
    discount_amount: Decimal
    shipping_fee: Decimal
    total_amount: Decimal

    customer_name: str
    customer_phone: str
    voucher_code: Optional[str]

    order_type: OrderType
    scheduled_time: Optional[datetime]
    delivery_address: Optional[str]

    payment_method: PaymentMethod
    payment_status: PaymentStatus
    status: OrderStatus

    created_at: datetime
    updated_at: datetime

    items: List[OrderItemResponseSchema]

    class Config:
        from_attributes = True


class AdminOrderItemOptionCreateSchema(BaseModel):
    option_value_id: int
class AdminOrderItemCreateSchema(BaseModel):
    product_variant_id: int
    quantity: int
    note: Optional[str] = None
    options: List[AdminOrderItemOptionCreateSchema] = []
class AdminOrderCreateSchema(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    order_type: OrderType
    delivery_address: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    payment_method: PaymentMethod
    payment_status: PaymentStatus
    items: List[AdminOrderItemCreateSchema]

