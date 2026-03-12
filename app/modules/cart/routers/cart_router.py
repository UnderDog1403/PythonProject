from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency
from app.core.security import get_current_user
from app.modules.cart.schemas.cart_schema import CalculateCartSchema, CartItemCreateSchema
from app.modules.cart.services.cart_service import CartService

CartRouter = APIRouter(
    prefix="/cart",
    tags=["Carts"]
)

@CartRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def get_cart(
    db : db_dependency,
    current_user = Depends(get_current_user)
):
    cart_service = CartService(db)
    user_id = current_user["id"]
    return await cart_service.get_cart(user_id)
@CartRouter.post(
    "/",
    status_code=status.HTTP_200_OK,
)
async def add_to_cart(
    payload: CartItemCreateSchema,
    db : db_dependency,
    current_user = Depends(get_current_user)
):
    cart_service = CartService(db)
    user_id = current_user["id"]
    return await cart_service.add_to_cart(user_id, payload.product_variant_id, payload.quantity)
@CartRouter.delete(
    "/remove/{variant_id}",
    status_code=status.HTTP_200_OK,
)
async def remove_item(
    variant_id: int,
    db : db_dependency,
    current_user = Depends(get_current_user)
):
    cart_service = CartService(db)
    user_id = current_user["user_id"]
    return await cart_service.remove_item(user_id, variant_id)
@CartRouter.delete(
    "/clear",
    status_code=status.HTTP_200_OK,
)
async def clear_cart(
    db : db_dependency,
    current_user = Depends(get_current_user)
):
    cart_service = CartService(db)
    user_id = current_user["user_id"]
    return await cart_service.clear_cart(user_id)
@CartRouter.post(
    "/update",
    status_code=status.HTTP_200_OK,
)
async def update_cart(
    product_variant_id: int,
    quantity: int,
    db : db_dependency,
    current_user = Depends(get_current_user)
):
    cart_service = CartService(db)
    user_id = current_user["id"]
    return await cart_service.update_cart_item(user_id, product_variant_id, quantity)
@CartRouter.post("/calculate")
async def calculate_selected_items(
    data: CalculateCartSchema,
    db : db_dependency,
    current_user=Depends(get_current_user)
):
    user_id = current_user["id"]
    cart_service = CartService(db)
    return await cart_service.calculate_selected_items(
        user_id=user_id,
        variant_ids=data.variant_ids
    )
