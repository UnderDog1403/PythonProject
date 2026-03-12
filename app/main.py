from fastapi import FastAPI

from app.modules.auth.routers.auth_router import AuthRouter
from app.modules.cart.routers.cart_router import CartRouter
from app.modules.product.routers.attribute_router import AttributeRouter
from app.modules.product.routers.attribute_value_router import AttributeValueRouter

from app.modules.product.routers.category_router import CategoryRouter
from app.modules.product.routers.option_router import OptionRouter
from app.modules.product.routers.option_value_router import OptionValueRouter
from app.modules.product.routers.product_option_router import ProductOptionRouter
from app.modules.product.routers.product_router import ProductRouter
from app.modules.product.routers.product_variant_router import ProductVariantRouter
from app.modules.product.routers.variant_attribute_value_router import VariantAttributeValueRouter
from app.modules.user.routers.user_router import UserRouter

app = FastAPI()
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

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}