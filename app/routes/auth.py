from fastapi import APIRouter, Depends, HTTPException, status
from app.db import get_db
from psycopg import Connection

from app.schemas.user_schemas import BaseUser
from app.schemas.user_schemas import UserIn, UserOut

from app import utils
from app.schemas.auth_schemas import (
    BaseRegisterSchema,
    RegisterCustomerSchema,
    RegisterEmployeeSchema,
)

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
def signin(user: UserIn, db: Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", (user.username,))
        db_user = cur.fetchone()

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials"
            )
        is_password_correct = utils.pwd_context.verify(
            user.password, db_user.get("password")
        )
        if not is_password_correct:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials"
            )
    return db_user
