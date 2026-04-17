import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from uvicorn import lifespan

from app.core.dependencies import db_dependency
from app.core.websocket import manager
from app.modules.auth.routers.auth_router import AuthRouter
from app.modules.cart.routers.cart_router import CartRouter
from app.modules.order.routers.order_router import OrderRouter, AdminOrderRouter
from app.modules.product.routers.attribute_router import AttributeRouter
from app.modules.product.routers.attribute_value_router import AttributeValueRouter

from app.modules.product.routers.category_router import CategoryRouter
from app.modules.product.routers.option_router import OptionRouter
from app.modules.product.routers.option_value_router import OptionValueRouter
from app.modules.product.routers.product_option_router import ProductOptionRouter
from app.modules.product.routers.product_router import ProductRouter
from app.modules.product.routers.product_variant_router import ProductVariantRouter
from app.modules.product.routers.variant_attribute_value_router import VariantAttributeValueRouter
from app.modules.promotion.routers.voucher_router import VoucherRouter
from app.modules.reservation.routers.dining_table_router import DiningTableRouter
from app.modules.reservation.routers.reservation_router import ReservationRouter, AdminReservationRouter
from app.modules.user.routers.user_router import UserRouter
from app.modules.reservation.services.dining_table_service import DiningTableService

service = DiningTableService(db_dependency)
async def table_status_loop():
    while True:
        tables = await service.admin_get_all_tables()

        await manager.broadcast({
            "type": "table_status",
            "data": tables
        })

        await asyncio.sleep(30)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    task = asyncio.create_task(table_status_loop())

    yield  # app chạy ở đây

    # SHUTDOWN
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
app = FastAPI(lifespan=lifespan)
app.include_router(UserRouter)
app.include_router(AuthRouter)
app.include_router(CategoryRouter)
app.include_router(ProductRouter)
app.include_router(ProductVariantRouter)
app.include_router(AttributeRouter)
app.include_router(AttributeValueRouter)
app.include_router(VariantAttributeValueRouter)
app.include_router(OptionRouter)
app.include_router(OptionValueRouter)
app.include_router(ProductOptionRouter)
app.include_router(CartRouter)
app.include_router(VoucherRouter)
app.include_router(OrderRouter)
app.include_router(AdminOrderRouter)
app.include_router(DiningTableRouter)
app.include_router(ReservationRouter)
app.include_router(AdminReservationRouter)


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}