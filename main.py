from fastapi import FastAPI

from modules.auth.routers.auth_router import AuthRouter
from modules.user.routers.user_router import UserRouter

app = FastAPI()
app.include_router(UserRouter)
app.include_router(AuthRouter)
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}