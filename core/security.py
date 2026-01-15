from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from uu import encode
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.sql.annotation import Annotated
from google.oauth2 import id_token
from google.auth.transport import requests
from modules.user.repositories.user_repository import UserRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM='HS256'
SECRET_KEY='T6d3gXj8Fq9zU1L0hK2aVwR7bM5eYp4XjAq1H8sV0cI'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_access_token( id: str, expires_delta: timedelta = None):
        encode = {'sub': id}
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

def get_user_current( token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id: str = payload.get("sub")
            user_current = UserRepository.get_user_by_id(id)
            if user_current is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return user_current
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )