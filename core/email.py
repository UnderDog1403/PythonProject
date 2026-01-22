from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from typing import List
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
    TEMPLATE_FOLDER ="templates"
)
fm= FastMail(conf)
def send_email(background_tasks: BackgroundTasks, subject: str, email_to: List[str], body: dict, template_name: str):
    message = MessageSchema(
        subject=subject,
        recipients=email_to,
        template_body=body,
        subtype=MessageType.html
    )
    background_tasks.add_task(fm.send_message, message, template_name= template_name)