from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
# BỎ import sqlalchemy.sql.functions.now đi nhé

from app.core.redis import redis_client
from app.modules.order.models.order_item_model import OrderItem
from app.modules.order.models.order_item_option_model import OrderItemOption
from app.modules.order.models.order_model import Order, DeliveryType
from app.modules.order.repositories.order_repository import OrderRepository
from app.modules.product.repositories.option_value_repository import OptionValueRepository
from app.modules.product.repositories.product_variant_repository import ProductVariantRepository
from app.modules.promotion.repositories.voucher_repository import VoucherRepository


class OrderService:
    def __init__(self, db: AsyncSession):
        self.order_repo = OrderRepository(db)
        self.db = db
        self.variant_repo = ProductVariantRepository(db)
        self.option_value_repo = OptionValueRepository(db)
        self.voucher_repo = VoucherRepository(db)

    async def get_by_id(self, order_id: int):
        order = await self.order_repo.get_by_id(order_id)
        return order
    async def update_status(self,order_id: int,data: dict):
        updated_order = await self.order_repo.update(order_id,data)
        return updated_order
    async def create(self, user_id: str, checkout_info: dict, selected_item_keys: list[str]):
        if not selected_item_keys:
            raise HTTPException(status_code=400, detail="Giỏ hàng không có sản phẩm nào được chọn.")

        # 1. TIỀN XỬ LÝ DICT: Bóc tách dữ liệu và ngăn lỗi kwargs
        voucher_code = checkout_info.pop("voucher_code", None)
        delivery_type_val = checkout_info.get("delivery_type")

        # 2. MỞ TRANSACTION
        async with self.db.begin():
            cart_key = f"cart:{user_id}"
            quantities = await redis_client.hmget(cart_key, selected_item_keys)

            parsed_selected = []
            all_v_ids = set()
            all_opt_ids = set()

            for key, qty in zip(selected_item_keys, quantities):
                if qty is None: continue

                v_id_str, opt_str = key.split(":")
                v_id = int(v_id_str)
                opts = [] if opt_str == "noopt" else list(map(int, opt_str.split("-")))

                all_v_ids.add(v_id)
                all_opt_ids.update(opts)
                parsed_selected.append({"item_key": key, "v_id": v_id, "opt_ids": opts, "qty": int(qty)})

            if not parsed_selected:
                raise HTTPException(400, "Sản phẩm trong giỏ hàng không hợp lệ.")

            variants_list = await self.variant_repo.get_by_ids(list(all_v_ids))
            variants = {v.id: v for v in variants_list if v.is_active}

            options_list = await self.option_value_repo.get_by_ids(list(all_opt_ids))
            options = {o.id: o for o in options_list}

            # Khởi tạo Order (Lúc này checkout_info đã sạch, không còn voucher_code)
            new_order = Order(
                user_id=str(user_id),
                subtotal=Decimal("0.0"),
                total_amount=Decimal("0.0"),
                **checkout_info
            )

            running_subtotal = Decimal("0.0")

            for item in parsed_selected:
                variant = variants.get(item["v_id"])
                if not variant:
                    raise HTTPException(400, "Có sản phẩm đã ngừng bán hoặc không tồn tại.")

                new_item = OrderItem(
                    product_variant_id=variant.id,
                    product_name=variant.product.name,
                    price=variant.price,
                    quantity=item["qty"]
                )

                item_total_price = variant.price
                for o_id in item["opt_ids"]:
                    opt_val = options.get(o_id)
                    if not opt_val: continue

                    new_opt = OrderItemOption(
                        option_id=opt_val.option_id,
                        option_value_id=opt_val.id,
                        option_name=opt_val.option.name,
                        option_value_name=opt_val.value,
                        extra_price=opt_val.extra_price
                    )
                    new_item.options.append(new_opt)
                    item_total_price += opt_val.extra_price

                new_order.items.append(new_item)
                running_subtotal += (item_total_price * item["qty"])

            # 3. LOGIC XỬ LÝ VOUCHER
            discount_amount = Decimal("0.0")
            applied_voucher_id = None

            if voucher_code:
                voucher = await self.voucher_repo.get_by_code_for_update(voucher_code)
                if not voucher:
                    raise HTTPException(400, "Mã giảm giá không tồn tại.")
                if not voucher.is_active:
                    raise HTTPException(400, "Mã giảm giá đã bị vô hiệu hóa.")

                current_time = datetime.now(timezone.utc)  # <-- Dùng datetime chuẩn của Python
                if current_time < voucher.start_at or current_time > voucher.end_at:
                    raise HTTPException(400, "Mã giảm giá không nằm trong thời gian áp dụng.")
                if voucher.used_count >= voucher.usage_limit:
                    raise HTTPException(400, "Mã giảm giá đã hết lượt sử dụng.")
                if running_subtotal < voucher.min_order_value:
                    raise HTTPException(400, f"Đơn hàng chưa đạt mức tối thiểu {voucher.min_order_value}đ.")

                if voucher.discount_type == "fixed":
                    discount_amount = voucher.discount_value
                elif voucher.discount_type == "percent":
                    calculated_discount = running_subtotal * (voucher.discount_value / Decimal("100.0"))
                    if voucher.max_discount_value and calculated_discount > voucher.max_discount_value:
                        discount_amount = voucher.max_discount_value
                    else:
                        discount_amount = calculated_discount

                if discount_amount > running_subtotal:
                    discount_amount = running_subtotal

                voucher.used_count += 1
                applied_voucher_id = voucher.id

            # 4. LOGIC PHÍ SHIP
            calculated_shipping_fee = Decimal("0.0")
            # Tùy theo cách truyền enum, phải check kỹ
            if delivery_type_val == DeliveryType.DELIVERY or delivery_type_val == "DELIVERY":
                calculated_shipping_fee = Decimal("10000.0")
                if not checkout_info.get("delivery_address"):
                    raise HTTPException(400, "Vui lòng nhập địa chỉ giao hàng tận nơi.")
            elif delivery_type_val == DeliveryType.PICKUP or delivery_type_val == "PICKUP":
                calculated_shipping_fee = Decimal("0.0")

            # 5. CHỐT ĐƠN VÀ LƯU DATABASE
            new_order.subtotal = running_subtotal
            new_order.discount_amount = discount_amount
            new_order.voucher_id = applied_voucher_id
            new_order.shipping_fee = calculated_shipping_fee
            new_order.total_amount = (running_subtotal - discount_amount) + calculated_shipping_fee

            await self.order_repo.create(new_order)

        # 6. DỌN DẸP REDIS (Sau khi DB Transaction đã hoàn tất an toàn)
        await redis_client.hdel(f"cart:{user_id}", *selected_item_keys)

        return new_order