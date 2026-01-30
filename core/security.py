
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.database import get_db
from modules.user.models.user_model import User



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM='HS256'
SECRET_KEY='T6d3gXj8Fq9zU1L0hK2aVwR7bM5eYp4XjAq1H8sV0cI'
VERIFY_KEY='T5d3gXj5Fq2zU1L0hK1aVwR7bM5eYp4XjAq1H8sV6cI'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
security = HTTPBearer()
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)
def create_reset_password_token( email: str, expires_delta: timedelta = None):
        encode = {
            'sub': email,
            'type': 'reset_password'
            }
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(hours=1)
        encode.update({"exp": expire})
        return jwt.encode(encode, VERIFY_KEY, algorithm=ALGORITHM)
def create_verify_token( id: str, expires_delta: timedelta = None):
        encode = {
            'sub': id,
            'type': 'verify'
            }
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(hours=24)
        encode.update({"exp": expire})
        return jwt.encode(encode, VERIFY_KEY, algorithm=ALGORITHM)
def verify_token(token: str):
        try:
            payload = jwt.decode(token, VERIFY_KEY, algorithms=[ALGORITHM])
            id: str = payload.get("sub")
            token_type: str = payload.get("type")
            if id is None or token_type != 'verify':
                raise ValueError ("Invalid token")
            return id
        except JWTError:
            raise ValueError("Invalid token")
def verify_reset_password_token(token: str):
        try:
            payload = jwt.decode(token, VERIFY_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            token_type: str = payload.get("type")
            if email is None or token_type != 'reset_password':
                raise ValueError ("Invalid token")
            return email
        except JWTError:
            raise ValueError("Invalid token")
def create_access_token( id: str,role: str, expires_delta: timedelta = None):
        encode = {'sub': id, 'role': role}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        encode.update({"exp": expire})
        return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
# def verify_google_token(token: str):
#     try:
#         idinfo = id_token.verify_oauth2_token(
#             token,
#             requests.Request(),
#             GOOGLE_CLIENT_ID
#         )
#         return idinfo
#     except ValueError:
#         return None


def decode_access_token(token: str) -> dict:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        return {
            "id": payload.get("sub"),
            "role": payload.get("role")
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
def require_roles(roles: list[str]):
    def checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return user
    return checker