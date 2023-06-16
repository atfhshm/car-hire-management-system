from fastapi import APIRouter, Depends, HTTPException, status
from app.db import get_db
from psycopg import Connection
from app.schemas.user_schemas import BaseUser

from app.utils import hash
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
                hash(user.password),
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
                hash(user.password),
                "EMPLOYEE",
            ),
        )
        new_user = cur.fetchone()
        db.commit()
    return new_user


@router.get("/signin")
def signin():
    return {"msg": "hello, world"}
