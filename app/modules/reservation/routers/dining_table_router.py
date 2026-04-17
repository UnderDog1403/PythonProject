from fastapi import APIRouter, FastAPI
from starlette import status
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.core.dependencies import db_dependency
from app.core.security import verify_token
from app.core.websocket import manager
from app.modules.reservation.schemas.dining_table_schema import DiningTableResponse, DiningTableCreate
from app.modules.reservation.services.dining_table_service import DiningTableService

DiningTableRouter = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)

router = APIRouter()
@router.websocket("/ws/tables")
async def websocket_tables_endpoint(
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

@DiningTableRouter.get(
    "/",
    status_code=status.HTTP_200_OK
)
async def get_all(
        db: db_dependency
):
    service = DiningTableService(db)
    result= await service.admin_get_all_tables()
    return result
@DiningTableRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(
        db:db_dependency,
        payload: DiningTableCreate
):
    service = DiningTableService(db)
    table = await service.create(payload.model_dump(exclude_unset=True))
    return table

