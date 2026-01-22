from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from ..schemas.auth_schema import LoginResponseSchema, LoginRequestSchema, login_form, RegisterRequestSchema, \
    register_form
from core.dependencies import db_dependency
from ..services.auth_service import AuthService

AuthRouter= APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
@AuthRouter.post("/login",response_model=LoginResponseSchema,status_code=status.HTTP_200_OK)
def login(
    payload: LoginRequestSchema,
    db: db_dependency,
    background_tasks: BackgroundTasks
):
    auth_service = AuthService(db, background_tasks)
    result = auth_service.login(payload.email, payload.password)
    return LoginResponseSchema(
        access_token=result["access_token"],
        user=result["user"]
    )

@AuthRouter.post("/register",status_code=status.HTTP_201_CREATED)
def register(
        payload: RegisterRequestSchema,
        db: db_dependency,
        background_tasks: BackgroundTasks
):
    auth_service = AuthService(db, background_tasks)
    return auth_service.register(payload.email, payload.password, payload.confirm_password)

@AuthRouter.get("/verify-email",status_code=status.HTTP_200_OK)
def verify_email(
        token: str,
        db: db_dependency,
        background_tasks: BackgroundTasks
):
    auth_service = AuthService(db, background_tasks)
    return auth_service.verify_email_token(token)


# @AuthRouter.post('/login/google',response_model=LoginResponseSchema, status_code=status.HTTP_200_OK)
# def google_login(
#         token: str,
#         auth_service = Depends(get_auth_service)
# ):
#         result = auth_service.login_google(token)
#         return LoginResponseSchema(
#             access_token=result["access_token"],
#             user=result["user"])

