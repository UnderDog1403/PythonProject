from sqlalchemy.orm import Session
from fastapi import Depends
# from sqlalchemy.sql.annotation import Annotated
from typing import Annotated


from modules.user.services.user_service import UserService
from core.database import SessionLocal
from modules.auth.services.auth_service import AuthService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
# auth_dependency = Annotated[id, Depends(AuthService.get_user_current)]
def get_user_service(
    db: db_dependency,
):
    return UserService(db)
def get_auth_service(db: db_dependency):
    return AuthService(db)