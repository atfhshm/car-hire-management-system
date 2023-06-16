from fastapi import status, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer

from jose import jwt, JWTError
from psycopg import Connection
from datetime import datetime, timedelta


from app.db import get_db
from app.schemas.user_schemas import TokenData
from .settings import settings


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRY_MINUTES = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


oath2_schema = OAuth2PasswordBearer(tokenUrl="login")


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
        username: str = payload.get("username")

        if not (id and username):
            raise credential_exception
    except JWTError:
        raise credential_exception

    return TokenData(**payload)


def get_current_user(
    token: str = Depends(oath2_schema), db: Connection = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = verify_access_token(
        token=token, credential_exception=credential_exception
    )
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s", (token_data.id))
        user = cur.fetchone()
    return user
