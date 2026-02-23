from fastapi import FastAPI

from app.modules.auth.routers.auth_router import AuthRouter
from app.modules.product.routers.category_router import CategoryRouter
from app.modules.product.routers.pizza_router import PizzaRouter
from app.modules.product.routers.pizza_size_router import PizzaSizeRouter
from app.modules.product.routers.pizza_topping_router import PizzaToppingRouter
from app.modules.user.routers.user_router import UserRouter
app = FastAPI()
app.include_router(UserRouter)
app.include_router(AuthRouter)
app.include_router(CategoryRouter)
app.include_router(PizzaRouter)
app.include_router(PizzaSizeRouter)
app.include_router(PizzaToppingRouter)
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}