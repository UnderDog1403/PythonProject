import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from starlette.background import BackgroundTasks

from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    verify_token,
    create_reset_password_token,
    verify_reset_password_token,
    create_refresh_token,
)
from app.modules.auth.models.auth_models import AuthProvider
from app.modules.auth.models.password_reset import PasswordReset
from app.modules.auth.repositories.auth_repository import AuthRepository
from app.modules.auth.services.email_service import (
    send_verification_email,
    send_forgot_password_email,
)
from app.modules.user.models.user_model import User
from app.modules.user.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: AsyncSession, background_tasks: BackgroundTasks):
        self.db = db
        self.user_repo = UserRepository(db)
        self.auth_repo = AuthRepository(db)
        self.background_tasks = background_tasks

    async def login(self, email: str, password: str):
        existing_user = await self.user_repo.get_user_by_email(email)

        if not existing_user:
            raise HTTPException(status_code=401, detail="Email or password is incorrect")

        if not existing_user.is_verified:
            raise HTTPException(status_code=403, detail="Email is not verified")

        if not existing_user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive")

        auth = await self.auth_repo.get_local_auth_by_user_id(existing_user.id)

        if not auth or not verify_password(password, auth.password_hash):
            raise HTTPException(status_code=401, detail="Email or password is incorrect")

        access_token = create_access_token(
            id=str(existing_user.id),
            role=existing_user.role.value,
        )
        refresh_token = create_refresh_token(
            id=str(existing_user.id),
            role=existing_user.role.value,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": existing_user,
        }


    async def change_password(self, user_id: str, new_password: str, confirm_password: str):
        if new_password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        auth = await self.auth_repo.get_local_auth_by_user_id(user_id)
        if not auth:
            raise HTTPException(status_code=404, detail="Authentication record not found")

        auth.password_hash = hash_password(new_password)
        await self.db.commit()

        return {"message": "Password changed successfully"}


    async def register(self, email: str, password: str, confirm_password: str):
        if password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        existing_user = await self.user_repo.get_user_by_email(email)

        if existing_user:
            existing_auth = await self.auth_repo.get_local_auth_by_user_id(existing_user.id)
            if existing_auth:
                raise HTTPException(status_code=409, detail="Email already exists")

            self.db.add(
                AuthProvider(
                    user_id=existing_user.id,
                    provider="local",
                    password_hash=hash_password(password),
                )
            )
            await self.db.commit()
            return {"message": "Local authentication added to existing user"}

        user_count = await self.user_repo.count_users()
        new_user = User(email=email, name=f"User{user_count + 1}")

        created_user = await self.user_repo.create_user(new_user)

        self.db.add(
            AuthProvider(
                user_id=created_user.id,
                provider="local",
                password_hash=hash_password(password),
            )
        )

        await self.db.commit()

        try:
            send_verification_email(created_user, self.background_tasks)
        except Exception as e:
            print("MAIL ERROR:", e)

        return {"message": "Registration successful. Please verify your email."}


    async def forget_password(self, email: str):
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        otp = "".join(secrets.choice("0123456789") for _ in range(6))

        self.db.add(
            PasswordReset(
                email=email,
                otp_hash=hash_password(otp),
                expired_at=datetime.now(timezone.utc) + timedelta(minutes=5),
            )
        )
        await self.db.commit()

        send_forgot_password_email(user, otp=otp, background_tasks=self.background_tasks)

        return {"message": "Password reset instructions sent"}


    async def verify_forgot_password_otp(self, email: EmailStr, otp: str):
        result = await self.db.execute(
            select(PasswordReset)
            .where(
                PasswordReset.email == email,
                PasswordReset.is_used == False,
            )
            .order_by(PasswordReset.created_at.desc())
        )
        password_reset = result.scalar_one_or_none()

        if (
            not password_reset
            or password_reset.expired_at <= datetime.now(timezone.utc)
            or not verify_password(otp, password_reset.otp_hash)
        ):
            raise HTTPException(status_code=400, detail="Invalid or expired OTP")

        password_reset.is_used = True
        await self.db.commit()

        return {
            "reset_token": create_reset_password_token(email),
            "message": "OTP verified successfully",
        }


    async def verify_email_token(self, token: str):
        try:
            user_id = verify_token(token)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_verified:
            raise HTTPException(status_code=400, detail="Email already verified")

        user.is_verified = True
        await self.db.commit()

        return {"message": "Email verified successfully"}


    async def reset_password(self, token: str, new_password: str, confirm_password: str):
        if new_password != confirm_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        try:
            email = verify_reset_password_token(token)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        auth = await self.auth_repo.get_local_auth_by_user_id(user.id)
        if not auth:
            raise HTTPException(status_code=404, detail="Authentication record not found")

        auth.password_hash = hash_password(new_password)
        await self.db.commit()

        return {"message": "Password reset successfully"}



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


