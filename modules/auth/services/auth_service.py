from sqlalchemy.orm import Session

from core.security import verify_password, hash_password, create_access_token
from modules.auth.models.auth_models import AuthProvider
from modules.auth.repositories.auth_repository import AuthRepository
from modules.user.models.user_model import User
from modules.user.repositories.user_repository import UserRepository



class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.auth_repo = AuthRepository(db)
    def login(self, email: str, password: str):
        existing_user = self.user_repo.get_user_by_email(email)
        if not existing_user:
            raise ValueError("Email or password is incorrect")
        auth = self.auth_repo.get_local_auth_by_user_id(existing_user.id)
        if not auth:
            raise ValueError("Authentication record not found")
        if not verify_password(password, auth.password_hash):
            raise ValueError("Email or password is incorrect")
        access_token = create_access_token(
            id=str(existing_user.id)
        )
        return {
            "access_token": access_token,
            "user": existing_user
        }
    def register(self,email:str,password: str,confirm_password:str):
        if password != confirm_password:
            raise ValueError("Password and Confirm Password do not match")
        existing_user = self.user_repo.get_user_by_email(email)
        if existing_user:
            existing_local_auth = self.auth_repo.get_local_auth_by_user_id(existing_user.id)
            if existing_local_auth:
                raise ValueError("Email already exists")
            new_local_auth = AuthProvider(
                user_id=existing_user.id,
                provider='local',
                password_hash=hash_password(password)
            )
            self.auth_repo.create_auth_provider(new_local_auth)
        else:
            user_count = self.user_repo.count_users()
            name = f"User{user_count + 1}"
            new_user = User(
                email=email,
                name=name
            )
            created_user = self.user_repo.create_user(new_user)
            new_local_auth = AuthProvider(
                user_id = created_user.id,
                provider='local',
                password_hash=hash_password(password)
            )
            self.auth_repo.create_auth_provider(new_local_auth)
        self.db.commit()
        return self.login(email=email, password=password)
    # def login_google(self,google_token: str):
    #     google_user = verify_google_token(google_token)
    #     if not google_user:
    #         raise ValueError("Invalid Google token")
    #     auth = self.auth_repo.get_google_auth_by_user_provider_id(google_user['sub'])
    #     if auth:
    #         user = self.user_repo.get_user_by_id(auth.user_id)
    #         access_token = create_access_token(
    #             id=str(user.id)
    #         )
    #         return {
    #             "access_token": access_token,
    #             "user": user
    #         }
    #     else:
    #         user = self.user_repo.get_user_by_email(google_user['email'])
    #         if not user:
    #             new_user = User(
    #                 email=google_user['email'],
    #                 name=google_user['name'],
    #                 image=google_user['picture']
    #             )
    #             user = self.user_repo.create_user(new_user)
    #         new_auth = AuthProvider(
    #             user_id=user.id,
    #             provider='google',
    #             provider_user_id=google_user['sub']
    #         )
    #         self.auth_repo.create_auth_provider(new_auth)
    #         access_token = create_access_token(
    #             id=str(user.id)
    #         )
    #         return {
    #             "access_token": access_token,
    #             "user": user
    #         }
    def logout(self):
        # For JWT, logout can be handled on the client side by deleting the token.
        return {"message": "Logout successful"}


