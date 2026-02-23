from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from typing import Annotated
from app.core.database import get_db

db_dependency = Annotated[AsyncSession, Depends(get_db)]
