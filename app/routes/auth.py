from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from psycopg import Connection

from app.schemas.user_schemas import BaseUser
from app.schemas.user_schemas import UserOut

from app import utils
from app import oauth
from app.db import get_db
from app.schemas.auth_schemas import RegisterCustomerSchema
from app.schemas.user_schemas import Token


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/customer-signup/", response_model=BaseUser)
def register_customer(user: RegisterCustomerSchema, db: Connection = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="passwords must match",
        )

    with db.cursor() as cur:
        cur.execute(
            """INSERT INTO users (username, email, first_name, last_name, password, type) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
            (
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                utils.hash(user.password),
                "CUSTOMER",
            ),
        )
        new_user = cur.fetchone()
        db.commit()
    return new_user


@router.post("/employee-signup/", response_model=BaseUser)
def register_employee(user: RegisterCustomerSchema, db: Connection = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="passwords must match",
        )

    with db.cursor() as cur:
        cur.execute(
            """INSERT INTO users (username, email, first_name, last_name, password, type) VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
            (
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                utils.hash(user.password),
                "EMPLOYEE",
            ),
        )
        new_user = cur.fetchone()
        db.commit()
    return new_user


@router.post("/signin", response_model=UserOut)
def signin(
    cred: OAuth2PasswordRequestForm = Depends(), db: Connection = Depends(get_db)
):
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", (cred.username,))
        db_user = cur.fetchone()

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials"
            )
        is_password_correct = utils.pwd_context.verify(
            cred.password, db_user.get("password")
        )
        if not is_password_correct:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials"
            )
        access_token = oauth.create_access_token(
            {"id": db_user.get("id"), "username": db_user.get("username")}
        )
    return {
        **db_user,
        "token": Token(access_token=access_token, toke_type="bearer"),
    }
