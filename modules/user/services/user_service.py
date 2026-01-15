from sqlalchemy.orm import Session

from core.security import hash_password
from ..models.user_model import User
from ..schemas.user_schema import UserRequestSchema
from ..repositories.user_repository import UserRepository

class UserService:
    def __init__(self,db: Session ):
        self.user_repo = UserRepository(db)
        self.db = db
    def get_user_by_email(self, email: str):
        return self.user_repo.get_user_by_email(email)
    def get_user_by_id(self, id: str):
        return self.user_repo.get_user_by_id(id)
    def create_user(self, user: User):
        existing_user = self.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("Email already exists")
        new_user = User(
            email=user.email,
            name = user.name,
            phone = user.phone,
            address= user.address,
            image = user.image,
        )
        return self.user_repo.create_user(new_user)

