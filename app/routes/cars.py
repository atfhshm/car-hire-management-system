from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from psycopg import Connection

from app.db import get_db

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("/")
def list_available_cars(db: Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("SELECT * FROM cars WHERE is_available = true")
        cars = cur.fetchall()
        if not cars:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return cars
