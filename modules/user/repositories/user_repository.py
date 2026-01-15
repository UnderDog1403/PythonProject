from sqlalchemy.orm import Session
from ..models.user_model import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_user_by_id(self, id):
        return self.db.query(User).filter(User.id == id).first()
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    def count_users(self):
        return self.db.query(User).count()
    def create_user(self, user: User):
        self.db.add(user)
        self.db.flush()
        return user

