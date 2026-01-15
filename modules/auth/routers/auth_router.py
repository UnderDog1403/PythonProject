from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.auth_schema import LoginResponseSchema, LoginRequestSchema, login_form, RegisterRequestSchema, \
    register_form
from core.dependencies import get_auth_service

AuthRouter= APIRouter(
    prefix="/auth",
    tags=["Auth"]
)
@AuthRouter.post("/login",response_model=LoginResponseSchema)
def login(
    auth: LoginRequestSchema= Depends(login_form),
    auth_service = Depends(get_auth_service)
):
    try:
        result = auth_service.login(auth.email, auth.password)
        return LoginResponseSchema(
            access_token=result["access_token"],
            user=result["user"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
@AuthRouter.post("/register",response_model=LoginResponseSchema)
def register(
        register: RegisterRequestSchema= Depends(register_form),
        auth_service = Depends(get_auth_service)
):
    try:
        result = auth_service.register(register.email, register.password, register.confirm_password)
        return LoginResponseSchema(
            access_token=result["access_token"],
            user=result["user"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
# @AuthRouter.post('/login/google',response_model=LoginResponseSchema)
# def google_login(
#         token: str,
#         auth_service = Depends(get_auth_service)
# ):
#     try:
#         result = auth_service.login_google(token)
#         return LoginResponseSchema(
#             access_token=result["access_token"],
#             user=result["user"]
#         )
#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e)
#         )
