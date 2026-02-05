from sqlalchemy.orm import Session
from ..models.user_model import User
from sqlalchemy import asc, desc
from typing import List, Optional, Any, Dict, Tuple
class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_user_by_id(self, id):
        return self.db.query(User).filter(User.id == id).first()
    def get_users_paginated(self, page: int = 1, limit: int = 10, order_by: str = "id",
                                 descending: bool = False) -> Tuple[List[User], int, int]:
        offset_value = max(page - 1, 0) * limit
        order_col = getattr(User, order_by, User.id)
        order_fn = desc if descending else asc

        total = self.db.query(User).count()

        items = (
            self.db.query(User)
            .order_by(order_fn(order_col))
            .offset(offset_value)
            .limit(limit)
            .all()
        )

        total_pages = (total + limit - 1) // limit if limit > 0 else 0
        return items, total, total_pages
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    def count_users(self):
        return self.db.query(User).count()
    def create_user(self, user: User):
        self.db.add(user)
        self.db.flush()
        return user
    def update_user(self, user_id: str, data: Dict[str, Any]) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        for key, value in data.items():
            if key == "id":
                continue
            if hasattr(user, key):
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    def update_active_status(self, user_id: str, is_active: bool) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        user.is_active = is_active
        self.db.commit()
        self.db.refresh(user)
        return user


