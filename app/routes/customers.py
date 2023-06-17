from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from psycopg import Connection

from app.db import get_db
from app import oauth
from app.schemas.customer_schemas import CustomerSchema, CustomerOut


router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/{id}", response_model=CustomerOut)
def get_customer(
    id: int, db: Connection = Depends(get_db), auth_user=Depends(oauth.get_current_user)
):
    with db.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        customer = cur.fetchone()
        if not customer or (customer.get("type") == "EMPLOYEE"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return customer


@router.put("/{id}", response_model=CustomerOut)
def update_customer(
    id: int,
    user: CustomerSchema,
    db: Connection = Depends(get_db),
    auth_user=Depends(oauth.get_current_user),
):
    with db.cursor() as cur:
        cur.execute(
            """UPDATE users SET username = %s, 
                                email = %s,
                                first_name = %s,
                                last_name = %s   
                                WHERE id = %s
                                RETURNING *
                                """,
            (user.username, user.email, user.first_name, user.last_name, id),
        )
        customer = cur.fetchone()
        if not customer or (customer.get("type") == "EMPLOYEE"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        db.commit()
    return customer


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    id: int, db: Connection = Depends(get_db), auth_user=Depends(oauth.get_current_user)
) -> None:
    with db.cursor() as cur:
        cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (id,))
        customer = cur.fetchone()
        if not customer or (customer.get("type") == "EMPLOYEE"):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        db.commit()
    return Response(
        status_code=status.HTTP_204_NO_CONTENT,
    )
