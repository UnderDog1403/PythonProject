from http.client import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_client
from app.modules.product.repositories.product_variant_repository import ProductVariantRepository


class CartService:
    def __init__(self, db: AsyncSession):
        self.variant_repository = ProductVariantRepository(db)


    async def get_cart(self,user_id: str):
        cart_key = f"cart:{user_id}"
        cart_items = await redis_client.hgetall(cart_key)
        items = []
        variant_ids = [int(v_id) for v_id in cart_items.keys()]

        variants = await self.variant_repository.get_by_ids(variant_ids)
        variant_map = {variant.id: variant for variant in variants}
        for variant_id, quantity in cart_items.items():

            variant_id = int(variant_id)
            quantity = int(quantity)

            variant = variant_map.get(variant_id)

            if not variant:
                await redis_client.hdel(cart_key, str(variant_id))
                continue

            items.append({
                "product_variant_id": variant.id,
                "product_name": variant.product.name,
                "quantity": quantity,
                "price": variant.price
            })

        return {"items": items}
    async def add_to_cart(self,user_id: str, product_variant_id: int, quantity: int):
        cart_key = f"cart:{user_id}"
        variant = await self.variant_repository.get_by_id(product_variant_id)

        if not variant:
            raise HTTPException(
                status_code=404,
                detail="Product variant not found"
            )

        if not variant.is_active:
            raise HTTPException(
                status_code=400,
                detail="Product variant is not available"
            )
        await redis_client.hincrby(cart_key, str(product_variant_id), quantity)
        await redis_client.expire(cart_key, 60 * 60 * 24 * 7)
        return {
            "variant_id": product_variant_id,
            "quantity": quantity
        }
    async def remove_item(self,user_id: str, variant_id: int):
        cart_key = f"cart:{user_id}"
        await redis_client.hdel(cart_key, variant_id)
        return {"message": "Item removed from cart"}
    async def clear_cart(self,user_id: str):
        cart_key = f"cart:{user_id}"
        await redis_client.delete(cart_key)
        return {"message": "Cart cleared"}
    async def update_cart_item(self,user_id: str, variant_id: int, quantity: int):
        cart_key = f"cart:{user_id}"
        if quantity <= 0:
            await redis_client.hdel(cart_key, variant_id)
            return {"message": "Item removed from cart"}
        await redis_client.hset(cart_key, variant_id, quantity)
        return {"message": "Cart item updated"}

    async def calculate_selected_items(self, user_id: str, variant_ids: list[int]):
        cart_key = f"cart:{user_id}"

        cart_items = await redis_client.hgetall(cart_key)

        if not cart_items:
            return {"items": [], "subtotal": 0}

        # query DB 1 lần
        variants = await self.variant_repository.get_by_ids(variant_ids)

        variant_map = {variant.id: variant for variant in variants}

        items = []
        subtotal = 0

        for variant_id in variant_ids:

            quantity = cart_items.get(str(variant_id))

            if not quantity:
                continue

            variant = variant_map.get(variant_id)

            if not variant:
                continue

            quantity = int(quantity)
            item_total = variant.price * quantity
            subtotal += item_total

            items.append({
                "product_variant_id": variant.id,
                "product_name": variant.product.name,
                "quantity": quantity,
                "price": variant.price,
                "total": item_total
            })

        return {
            "items": items,
            "subtotal": subtotal
        }

