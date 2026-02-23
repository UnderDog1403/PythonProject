from pathlib import Path

from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from typing import List

BASE_DIR = Path(__file__).resolve().parent.parent  # app
TEMPLATE_FOLDER = BASE_DIR / "templates"
conf = ConnectionConfig(
    MAIL_USERNAME ="phamducanh1906@gmail.com",
    MAIL_PASSWORD = "ylyw xxsv bmdi hfhp",
    MAIL_FROM = "phamducanh1906@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
    TEMPLATE_FOLDER= TEMPLATE_FOLDER
)
fm= FastMail(conf)
async def send_email_async(
    subject: str,
    email_to: List[str],
    body: dict,
    template_name: str
):
    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        template_body=body,
        subtype=MessageType.html,
    )

    await fm.send_message(message, template_name=template_name)