from fastapi import APIRouter
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.core.database import AsyncSessionLocal
from app.core.security import decode_access_token
from app.core.websocket import manager
from app.modules.reservation.services.dining_table_service import DiningTableService

router = APIRouter()
@router.websocket("/ws/tables")
async def websocket_tables_endpoint(
    websocket: WebSocket
):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    user = decode_access_token(token)
    user_id_str = str(user["sub"]) if user else None
    print("USER:", user_id_str)
    if user_id_str is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    await manager.connect(websocket, user_id_str)
    async with AsyncSessionLocal() as db:
        service = DiningTableService(db)
        tables = await service.admin_get_all_tables()
        await websocket.send_json({
            "type": "init",
            "data": tables
        })
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id_str)