from http.client import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_client
from app.modules.product.repositories.option_repository import OptionRepository
from app.modules.product.repositories.option_value_repository import OptionValueRepository
from app.modules.product.repositories.product_variant_repository import ProductVariantRepository


class CartService:
    def __init__(self, db: AsyncSession):
        self.variant_repository = ProductVariantRepository(db)
        self.option_repository = OptionRepository(db)
        self.option_value_repository = OptionValueRepository(db)

    async def get_cart(self, user_id: str):
        cart_key = f"cart:{user_id}"
        cart_data = await redis_client.hgetall(cart_key)
        if not cart_data:
            return {"items": []}

        all_variant_ids = set()
        all_option_ids = set()
        parsed_items = []

        for key, quantity in cart_data.items():
            key = key.decode() if isinstance(key, bytes) else key
            v_id_str, opt_str = key.split(":")
            v_id = int(v_id_str)
            opts = [] if opt_str == "noopt" else list(map(int, opt_str.split("-")))

            all_variant_ids.add(v_id)
            all_option_ids.update(opts)
            parsed_items.append({"v_id": v_id, "opt_ids": opts, "qty": int(quantity)})


        variants = {v.id: v for v in await self.variant_repository.get_by_ids(list(all_variant_ids)) if v.is_active}
        options = {o.id: o for o in await self.option_value_repository.get_by_ids(list(all_option_ids)) }


        final_items = []

        for item in parsed_items:
            variant = variants.get(item["v_id"])
            if not variant: continue

            item_options = [options[o_id] for o_id in item["opt_ids"] if o_id in options]
            option_total = sum(opt.extra_price for opt in item_options)

            item_total = (variant.price + option_total) * item["qty"]

            final_items.append({
                "item_key": f"{variant.id}:{'-'.join(map(str, sorted(item['opt_ids'])))}",
                "variant_id": variant.id,
                "price": variant.price,
                "name": variant.product.name,
                "quantity": item["qty"],
                "options": [{"id": o.id, "value": o.value, "price": o.extra_price} for o in item_options],
                "item_total": item_total
            })

        return {"items": final_items}

    async def add_to_cart(
            self,
            user_id: str,
            product_variant_id: int,
            quantity: int,
            option_value_ids: list[int]
    ):
        if quantity <= 0:
            raise HTTPException(400, "Invalid quantity")
        variant = await self.variant_repository.get_by_id(product_variant_id)
        if not variant or not variant.is_active:
            raise HTTPException(400, "Variant not available")
        option_value_key = "-".join(map(str, sorted(option_value_ids))) if option_value_ids else "noopt"

        cart_item_key = f"{product_variant_id}:{option_value_key}"
        cart_key = f"cart:{user_id}"

        await redis_client.hincrby(cart_key, cart_item_key, quantity)
        await redis_client.expire(cart_key, 60 * 60 * 24 * 7)
        return {
            "product_variant_id": product_variant_id,
            "option_values": option_value_ids,
            "quantity": quantity
        }

    async def remove_item(self, user_id: str, item_key: str):
        cart_key = f"cart:{user_id}"
        await redis_client.hdel(cart_key, item_key)
        return {"message": "Item removed from cart"}

    async def update_cart_item(self, user_id: str, item_key: str, quantity: int):
        if quantity <= 0:
            return await self.remove_item(user_id, item_key)

        cart_key = f"cart:{user_id}"

        exists = await redis_client.hexists(cart_key, item_key)
        if not exists:
            raise HTTPException(404, "Item not found in cart")


        await redis_client.hset(cart_key, item_key, quantity)
        return {"message": "Updated quantity", "item_key": item_key, "quantity": quantity}

    async def clear_cart(self, user_id: str):
        cart_key = f"cart:{user_id}"
        await redis_client.delete(cart_key)
        return {"message": "Cart cleared successfully"}

