from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.modules.auth.models.auth_models import AuthProvider, AuthProviderEnum


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_auth_by_user_id(self, user_id):
        result = await self.db.execute(
            select(AuthProvider).where(AuthProvider.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_local_auth_by_user_id(self, user_id):
        result = await self.db.execute(
            select(AuthProvider).where(
                AuthProvider.user_id == user_id,
                AuthProvider.provider == AuthProviderEnum.local
            )
        )
        return result.scalar_one_or_none()

    async def get_google_auth_by_user_provider_id(self, provider_user_id):
        result = await self.db.execute(
            select(AuthProvider).where(
                AuthProvider.provider == AuthProviderEnum.google,
                AuthProvider.provider_user_id == provider_user_id
            )
        )
        return result.scalar_one_or_none()

    async def create_auth_provider(self, auth_provider: AuthProvider):
        self.db.add(auth_provider)
        await self.db.flush()   # để có id ngay nếu cần
        return auth_provider
