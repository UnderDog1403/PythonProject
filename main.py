from fastapi import FastAPI

from modules.auth.routers.auth_router import AuthRouter
from modules.product.routers.category_router import CategoryRouter
from modules.product.routers.pizza_router import PizzaRouter
from modules.user.routers.user_router import UserRouter

app = FastAPI()
app.include_router(UserRouter)
app.include_router(AuthRouter)
app.include_router(CategoryRouter)
app.include_router(PizzaRouter)
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}