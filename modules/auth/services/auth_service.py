from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from core.security import verify_password, hash_password, create_access_token, create_verify_token, verify_token
from modules.auth.models.auth_models import AuthProvider
from modules.auth.repositories.auth_repository import AuthRepository
from modules.auth.services.email_service import send_verification_email
from modules.user.models.user_model import User
from modules.user.repositories.user_repository import UserRepository



class AuthService:
    def __init__(self, db: Session, background_tasks: BackgroundTasks):
        self.db = db
        self.user_repo = UserRepository(db)
        self.auth_repo = AuthRepository(db)
        self.background_tasks = background_tasks
    def login(self, email: str, password: str):
        existing_user = self.user_repo.get_user_by_email(email)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or password is incorrect"
            )
        if not existing_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email is not verified"
            )
        if not existing_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        auth = self.auth_repo.get_local_auth_by_user_id(existing_user.id)
        if not auth:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication record not found"
            )
        if not verify_password(password, auth.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email or password is incorrect"
            )
        access_token = create_access_token(
            id=str(existing_user.id)
        )
        return {
            "access_token": access_token,
            "user": existing_user
        }


    def register(self,email:str,password: str,confirm_password:str):
        if password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and Confirm Password do not match"
            )
        existing_user = self.user_repo.get_user_by_email(email)
        if existing_user:
            existing_local_auth = self.auth_repo.get_local_auth_by_user_id(existing_user.id)
            if existing_local_auth:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists"
                )
            new_local_auth = AuthProvider(
                user_id=existing_user.id,
                provider='local',
                password_hash=hash_password(password)
            )
            self.auth_repo.create_auth_provider(new_local_auth)
            self.db.commit()
            return {"message": "Local authentication added to existing user"}
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
            send_verification_email(created_user, background_tasks=self.background_tasks)
            return {"message": "Registration successful. Please verify your email."}
            # return self.login(email=email, password=password)

    def verify_email_token(self, token: str):
        id= verify_token(token)
        user=self.user_repo.get_user_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )
        if user.is_verified:
            return {"message": "Email is already verified"}
        user.is_verified = True
        self.db.commit()
        return {"message": "Email verified successfully"}
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


