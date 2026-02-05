import secrets
from datetime import datetime, timedelta,timezone

from fastapi import HTTPException,status
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.background import BackgroundTasks

from core.security import verify_password, hash_password, create_access_token, create_verify_token, verify_token, \
    create_reset_password_token, verify_reset_password_token, create_refresh_token
from modules.auth.models.auth_models import AuthProvider
from modules.auth.models.password_reset import PasswordReset
from modules.auth.repositories.auth_repository import AuthRepository
from modules.auth.services.email_service import send_verification_email, send_forgot_password_email
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
            id=str(existing_user.id),
            role = existing_user.role.value
        )
        refresh_token = create_refresh_token(
            id=str(existing_user.id),
            role = existing_user.role.value
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": existing_user
        }

    def change_password(self,user_id:str, new_password:str, confirm_password:str):
        if new_password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New Password and Confirm Password do not match"
            )
        auth = self.auth_repo.get_local_auth_by_user_id(user_id)
        if not auth:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Authentication record not found"
            )
        auth.password_hash = hash_password(new_password)
        self.db.commit()
        return {"message": "Password changed successfully"}
    
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
    def forget_password(self,email: str):
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with this email does not exist"
            )
        otp = ''.join(secrets.choice('0123456789') for _ in range(6))
        self.db.add(
            PasswordReset(
                email=email,
                otp_hash=hash_password(otp),
                expired_at = datetime.now(timezone.utc) + timedelta(minutes=5)
            )
        )
        self.db.commit()
        send_forgot_password_email(user, background_tasks=self.background_tasks,otp=otp)
        return {"message": "Password reset instructions have been sent to your email"}
    def verify_forgot_password_otp(self,email: EmailStr, otp: str):
        password_reset = self.db.query(PasswordReset).filter(
            PasswordReset.email==email,
            PasswordReset.is_used==False
        ).order_by(PasswordReset.created_at.desc()).first()
        if not password_reset:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP"
            )
        if password_reset.expired_at <= datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired"
            )
        if not verify_password(otp, password_reset.otp_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )
        token = create_reset_password_token(email)
        password_reset.is_used = True
        self.db.commit()
        return {
            "reset_token": token,
            "message": "OTP verified successfully"}

    def verify_email_token(self, token: str):
        try:
            id= verify_token(token)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired token"
            )
        user=self.user_repo.get_user_by_id(id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )
        if user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already verified"
            )
        user.is_verified = True
        self.db.commit()
        return {"message": "Email verified successfully"}
    def reset_password(self, token: str, new_password: str, confirm_password: str):
        if new_password != confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New Password and Confirm Password do not match"
            )
        try:
            email = verify_reset_password_token(token)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token"
            )
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        auth = self.auth_repo.get_local_auth_by_user_id(user.id)
        if not auth:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Authentication record not found"
            )
        auth.password_hash = hash_password(new_password)
        self.db.commit()
        return {"message": "Password has been reset successfully"}
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


