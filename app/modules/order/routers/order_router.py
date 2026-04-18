from fastapi import APIRouter, Depends
from starlette import status
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.core.dependencies import db_dependency
from app.core.security import get_current_user, verify_token, require_roles
from app.core.websocket import manager
from app.modules.order.schemas.order_schema import CheckoutRequest, OrderStatusUpdate, AdminOrderCreateSchema, \
    OrderResponseSchema
from app.modules.order.services.order_service import OrderService
router = APIRouter()
OrderRouter = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)
AdminOrderRouter = APIRouter(
    prefix="/admin/orders",
    tags=["Admin Orders"]
)

# ADMIN CREATE ORDER
@AdminOrderRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def admin_create(
    payload: AdminOrderCreateSchema,
    db : db_dependency,
    current_user=Depends(require_roles(["admin"]))
):
    order_service = OrderService(db)
    user_id = payload.checkout_info.user_id
    return await order_service.create(user_id,payload.checkout_info.model_dump(),payload.selected_items)









# ADMIN UPDATE ORDER STATUS
@AdminOrderRouter.patch(
    "/{order_id}/status",
    status_code=status.HTTP_200_OK,
)
async def update_order_status(
        order_id: int,
        db: db_dependency,
        payload: OrderStatusUpdate
):
    order_service = OrderService(db)
    updated_order = await order_service.update_status(order_id, payload.model_dump())
    if updated_order:
        owner_id = str(updated_order["user_id"])
        updated_data = {
            "event": "ORDER_STATUS_CHANGED",
            "data": {
                "order_id": order_id,
                "new_status": payload.status,
                "message": f"Đơn hàng #{order_id} đã chuyển sang trạng thái: {payload.status}"
            }
        }
        await manager.send_personal_message(updated_data, owner_id)
    return updated_order

# ADMIN GET ALL ORDER BY USER_ID
@AdminOrderRouter.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
)
async def admin_get_all_by_user(
    user_id: str,
    db : db_dependency,
    current_user=Depends(require_roles(["admin"]))
):
    order_service = OrderService(db)
    return await order_service.get_all_by_user_id(user_id)

# ADMIN GET ALL ORDER
@AdminOrderRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def admin_get_all(
    db : db_dependency,
    current_user=Depends(require_roles(["admin"]))
):
    order_service = OrderService(db)
    return await order_service.admin_get_all()

# ADMIN GET ORDER DETAIL BY ORDER_ID
@AdminOrderRouter.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
)
async def admin_get_by_id(
    order_id: int,
    db : db_dependency,
    current_user=Depends(require_roles(["admin"]))
):
    order_service = OrderService(db)
    return await order_service.admin_get_by_id(order_id)

#USER CREATE ORDER

@OrderRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderResponseSchema
)
async def create(
    payload: CheckoutRequest,
    db : db_dependency,
    current_user=Depends(get_current_user)
):
    order_service = OrderService(db)
    user_id = current_user['id']
    return await order_service.create(user_id,payload.checkout_info.model_dump(),payload.selected_items)

# USER GET ORDER BY USER_ID
@OrderRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_all_by_user(
    db : db_dependency,
    current_user=Depends(get_current_user)
):
    order_service = OrderService(db)
    user_id = current_user['id']
    return await order_service.get_all_by_user_id(user_id)

#USER GET ORDER DETAIL BY ORDER_ID
@OrderRouter.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
)
async def get_by_id(
    order_id: int,
    db : db_dependency,
    current_user=Depends(get_current_user)
):
    order_service = OrderService(db)
    user_id = current_user['id']
    return await order_service.get_by_id_and_user(order_id,user_id)
@OrderRouter.patch(
    "/{order_id}/cancel",
    status_code=status.HTTP_200_OK,
)

#USER CANCEL ORDER BY ORDER_ID

async def cancel_order(
    order_id: int,
    db : db_dependency,
    current_user=Depends(get_current_user)
):
    order_service = OrderService(db)
    user_id = current_user['id']
    return await order_service.cancel_order(order_id,user_id)

