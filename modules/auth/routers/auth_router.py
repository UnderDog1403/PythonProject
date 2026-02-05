
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks

from core.security import require_roles
from ..schemas.auth_schema import LoginResponseSchema, LoginRequestSchema, login_form, RegisterRequestSchema, \
    register_form, ChangePasswordRequestSchema, ForgotPasswordRequestSchema, VerifyForgotPasswordRequestSchema
from core.dependencies import db_dependency
from ..services.auth_service import AuthService
from fastapi import Header

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

@AuthRouter.post("/change-password",status_code=status.HTTP_200_OK)
def change_password(
        payload: ChangePasswordRequestSchema,
        db: db_dependency,
        background_tasks: BackgroundTasks,
        current_user=Depends(require_roles(["user", "admin"]))
):
    service = AuthService(db, background_tasks)
    return service.change_password(
        current_user["id"],
        payload.new_password,
        payload.confirm_password
    )
@AuthRouter.post("/forgot-password",status_code=status.HTTP_200_OK)
def forgot_password(
        payload: ForgotPasswordRequestSchema,
        db: db_dependency,
        background_tasks: BackgroundTasks
):
    service = AuthService(db, background_tasks)
    return service.forget_password(payload.email)

@AuthRouter.post("/verify-forgot-password-otp",status_code=status.HTTP_200_OK)
def verify_forgot_password_otp(
        payload: VerifyForgotPasswordRequestSchema,
        db: db_dependency,
        background_tasks: BackgroundTasks
):
    service = AuthService(db, background_tasks)
    return service.verify_forgot_password_otp(payload.email, payload.otp)
@AuthRouter.post("/reset-password",status_code=status.HTTP_200_OK)
def reset_password(
        payload: ChangePasswordRequestSchema,
        db: db_dependency,
        background_tasks: BackgroundTasks,
        reset_token: str = Header(..., alias="X-Reset-Token"),
):
    service = AuthService(db, background_tasks)
    return service.reset_password(
        reset_token,
        payload.new_password,
        payload.confirm_password
    )

# @AuthRouter.post('/login/google',response_model=LoginResponseSchema, status_code=status.HTTP_200_OK)
# def google_login(
#         token: str,
#         auth_service = Depends(get_auth_service)
# ):
#         result = auth_service.login_google(token)
#         return LoginResponseSchema(
#             access_token=result["access_token"],
#             user=result["user"])

