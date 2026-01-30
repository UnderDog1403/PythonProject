from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from core.security import hash_password
from ..models.user_model import User
from ..repositories.user_repository import UserRepository

class UserService:
    def __init__(self,db: Session ):
        self.user_repo = UserRepository(db)
        self.db = db
    def get_users_paginated(self, page: int =1, limit: int =10):
        if not self.user_repo.get_users_paginated(page, limit):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not found users"
            )
        return self.user_repo.get_users_paginated(page, limit)
    def get_user_by_id(self, id: str):
        if not self.user_repo.get_user_by_id(id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return self.user_repo.get_user_by_id(id)



