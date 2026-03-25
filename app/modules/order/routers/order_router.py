from fastapi import APIRouter, Depends
from starlette import status
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.core.dependencies import db_dependency
from app.core.security import get_current_user, verify_token
from app.core.websocket import manager
from app.modules.order.schemas.order_schema import CheckoutRequest, OrderStatusUpdate
from app.modules.order.services.order_service import OrderService
router = APIRouter()
OrderRouter = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)
@router.websocket("ws/orders")
async def websocket_orders_endpoint(
    websocket: WebSocket,
    token: str
):
    user_id_str = verify_token(token)
    if user_id_str is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, user_id_str)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id_str)
@OrderRouter.put("admin/{order_id}/status")
async def update_order_status(
        order_id: int,
        db: db_dependency,
        payload: OrderStatusUpdate
):
    order_service = OrderService(db)
    updated_order = order_service.update_status(order_id, payload.model_dump())
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
@OrderRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(
    payload: CheckoutRequest,
    db : db_dependency,
    current_user=Depends(get_current_user)
):
    order_service = OrderService(db)
    user_id = current_user['id']
    await order_service.create(user_id,payload.checkout_info.model_dump(),payload.selected_items)

