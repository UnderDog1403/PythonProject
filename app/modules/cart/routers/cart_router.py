from fastapi import APIRouter, Depends
from starlette import status

from app.core.dependencies import db_dependency
from app.core.security import get_current_user
from app.modules.cart.schemas.cart_schema import CalculateCartSchema, CartItemCreateSchema, RemoveCartItemSchema, \
    CartItemUpdateSchema, CartResponse, CalculateResponse
from app.modules.cart.services.cart_service import CartService

CartRouter = APIRouter(
    prefix="/cart",
    tags=["Carts"]
)

@CartRouter.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CartResponse
)
async def get_cart(
    db : db_dependency,
    current_user = Depends(get_current_user),
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
    return await cart_service.add_to_cart(user_id, payload.product_variant_id, payload.quantity,payload.option_value_ids)
@CartRouter.delete(
    "/remove",
    status_code=status.HTTP_200_OK,
)
async def remove_item(
    payload: RemoveCartItemSchema,
    db : db_dependency,
    current_user = Depends(get_current_user)
):
    cart_service = CartService(db)
    user_id = current_user["id"]
    return await cart_service.remove_item(user_id, payload.item_key)
@CartRouter.delete(
    "/",
    status_code=status.HTTP_200_OK,
)
async def clear_cart(
    db : db_dependency,
    current_user = Depends(get_current_user)
):
    cart_service = CartService(db)
    user_id = current_user["id"]
    return await cart_service.clear_cart(user_id)
@CartRouter.patch(
    "/",
    status_code=status.HTTP_200_OK,
)
async def update_cart(
    payload: CartItemUpdateSchema,
    db : db_dependency,
    current_user = Depends(get_current_user)
):
    cart_service = CartService(db)
    user_id = current_user["id"]
    return await cart_service.update_cart_item(user_id, payload.item_key,payload.quantity)
