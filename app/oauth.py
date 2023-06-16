from fastapi import status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer

from jose import jwt, JWTError
from psycopg import Connection
from datetime import datetime, timedelta


from app.db import get_db

from .settings import Settings

settings = Settings()


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRY_MINUTES = timedelta(minutes=settings.access_token_expire_minutes)


oath2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(
    data: dict, expiry_delta: timedelta = ACCESS_TOKEN_EXPIRY_MINUTES
):
    to_encode = data.copy()
    if expiry_delta:
        expire_at = datetime.now() + expiry_delta
    else:
        expire_at = datetime.now() + timedelta(minutes=50)

    to_encode.update({"exp": expire_at})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credential_exception: Exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("id")
        email: str = payload.get("email")

        if not (id and email):
            raise credential_exception
    except JWTError:
        raise credential_exception

    return schema.TokenData(**payload)


def get_current_user(
    token: str = Depends(oath2_schema), db: Connection = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(
        token=token, credential_exception=credential_exception
    )
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user
