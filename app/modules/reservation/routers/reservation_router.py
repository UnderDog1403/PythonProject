from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency
from app.core.security import get_current_user
from app.modules.reservation.schemas.reservation_schema import ReservationResponse, ReservationCreate, \
    ReservationFilter, AdminConfirmReservationRequest, AdminReservationCreate, AdminReservationUpdate
from app.modules.reservation.services.reservation_service import ReservationService

ReservationRouter = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)
AdminReservationRouter = APIRouter(
    prefix="/admin/reservations",
    tags=["Admin Reservations"]
)
# @ReservationRouter.get(
#     "/",
#     status_code=status.HTTP_200_OK,
#     response_model=list[ReservationResponse]
# )
# async def get_all(
#         db: db_dependency
# ):
#     service = ReservationService(db)
#     tables= await service.get_all()
#     return tables
@ReservationRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create(
        db:db_dependency,
        payload: ReservationCreate,
        current_user = Depends(get_current_user),
):
    service = ReservationService(db)
    data = payload.model_dump(exclude_unset=True)
    data["user_id"] = current_user["id"]
    result = await service.create(data)
    return result
@ReservationRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[ReservationResponse]
)
async def user_get_reservations(
        db: db_dependency,
        current_user = Depends(get_current_user),
):
    service = ReservationService(db)
    reservations = await service.user_get_reservations(current_user["id"])
    return reservations
@AdminReservationRouter.post(
    "/filter",
    status_code=status.HTTP_200_OK,
    response_model=list[ReservationResponse]
)
async def filter_reservations(
        db: db_dependency,
        payload: ReservationFilter
):
    service = ReservationService(db)
    reservations = await service.admin_filter_reservations(payload.model_dump(exclude_unset=True))
    return reservations
@AdminReservationRouter.get(
    "/{reservation_id}/available-tables",
    status_code=status.HTTP_200_OK,
)
async def get_available_tables(
        db: db_dependency,
        reservation_id: int
):
    service = ReservationService(db)
    tables = await service.admin_get_available_tables_for_reservation(reservation_id)
    return tables
@AdminReservationRouter.put(
    "/{reservation_id}/confirm",
    status_code=status.HTTP_200_OK
)
async def confirm_reservation(
        db: db_dependency,
        reservation_id: int,
        payload: AdminConfirmReservationRequest
):
    service = ReservationService(db)
    reservation = await service.admin_confirm_reservation(reservation_id, payload.table_ids)
    return reservation
@AdminReservationRouter.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def admin_create_reservation(
        db: db_dependency,
        payload: AdminReservationCreate
):
    service = ReservationService(db)
    result = await service.create(payload.model_dump(exclude_unset=True))
    return result
@AdminReservationRouter.put(
    "/{reservation_id}",
    status_code=status.HTTP_200_OK
)
async def admin_update_reservation(
        db: db_dependency,
        reservation_id: int,
        payload: AdminReservationUpdate
):
    service = ReservationService(db)
    reservation = await service.admin_update_reservation(reservation_id, payload.model_dump(exclude_unset=True))
    return reservation

