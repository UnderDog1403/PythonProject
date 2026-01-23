from fastapi import BackgroundTasks
from core.email import send_email
from core.security import create_verify_token
from modules.user.models.user_model import User


def send_verification_email(user: User, background_tasks: BackgroundTasks):
    token = create_verify_token(
        id =str(user.id)
    )
    active_url = f"http://localhost:8000/auth/verify-email?token={token}"
    subject = "Verify your email"
    body = {
        "name": user.name,
        "active_url": active_url
    }
    send_email(
        email_to =[user.email],
        subject=subject,
        body=body,
        background_tasks=background_tasks,
        template_name="verify_email_account.html"
    )
def send_forgot_password_email(user: User, background_tasks: BackgroundTasks,otp:str):
    subject = "Reset your password"
    body = {
        "name": user.name,
        'otp': otp
    }
    send_email(
        email_to =[user.email],
        subject=subject,
        body=body,
        background_tasks=background_tasks,
        template_name="forgot_password.html"
    )

