from sqlalchemy.orm import Session
from ..models.user_model import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_user_by_id(self, id):
        return self.db.query(User).filter(User.id == id).first()
    def get_users_paginated(self, page: int = 1, limit: int = 10):
        total = self.db.query(User).count()
        total_pages = (total + limit - 1) // limit
        if page < 1 or page > total_pages:
            return [], total , total_pages
        users = self.db.query(User).order_by(User.updated_at.desc()).offset((page-1) * limit).limit(limit).all()
        return users, total, total_pages
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    def count_users(self):
        return self.db.query(User).count()
    def create_user(self, user: User):
        self.db.add(user)
        self.db.flush()
        return user

