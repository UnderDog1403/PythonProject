from sqlalchemy.orm import Session
from fastapi import Depends
from sqlalchemy.sql.annotation import Annotated
from typing import Annotated

from core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
# auth_dependency = Annotated[id, Depends(AuthService.get_user_current)]
