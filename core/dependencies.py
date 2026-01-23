from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from core.database import get_db
from core.security import get_user_current
from modules.user.models.user_model import User




db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[User, Depends(get_user_current)]


