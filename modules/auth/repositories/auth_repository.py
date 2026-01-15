from sqlalchemy.orm import Session
from modules.auth.models.auth_models import AuthProvider, AuthProviderEnum


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db
    def get_auth_by_user_id(self, user_id):
        return self.db.query(AuthProvider).filter(AuthProvider.user_id == user_id).first()
    def get_local_auth_by_user_id(self, user_id):
        return self.db.query(AuthProvider).filter(
            AuthProvider.user_id == user_id,
            AuthProvider.provider == AuthProviderEnum.local
        ).first()
    def get_google_auth_by_user_provider_id(self, provider_user_id):
        return self.db.query(AuthProvider).filter(
            AuthProvider.provider == AuthProviderEnum.google,
            AuthProvider.provider_user_id == provider_user_id
        ).first()
    def create_auth_provider(self, auth_provider: AuthProvider):
        self.db.add(auth_provider)
        return auth_provider

