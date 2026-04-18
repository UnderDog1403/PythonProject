from fastapi import APIRouter
from starlette import status


from app.core.dependencies import db_dependency
from app.modules.reservation.schemas.dining_table_schema import DiningTableResponse, DiningTableCreate
from app.modules.reservation.services.dining_table_service import DiningTableService

DiningTableRouter = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)



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

