from pydantic import BaseModel,EmailStr
from fastapi import Depends, Form
from modules.user.schemas.user_schema import UserResponseSchema


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str

async def login_form(
    email: EmailStr = Form(...),
    password: str = Form(...)
):
    return LoginRequestSchema(email=email, password=password)
class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchema
    class Config:
        from_attributes = True
class RegisterRequestSchema(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str
async def register_form(
    email: EmailStr = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    return RegisterRequestSchema(email=email, password=password, confirm_password=confirm_password)
class ChangePasswordRequestSchema(BaseModel):
    new_password: str
    confirm_password: str
class ForgotPasswordRequestSchema(BaseModel):
    email: EmailStr
class VerifyForgotPasswordRequestSchema(BaseModel):
    email: EmailStr
    otp: str

