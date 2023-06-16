from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from psycopg import Connection

from app.db import get_db
from app.schemas.cars_schemas import CarSchema, BookingSchema

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("/")
def list_available_cars(db: Connection = Depends(get_db)) -> list[CarSchema]:
    with db.cursor() as cur:
        cur.execute("SELECT * FROM cars WHERE is_available = true")
        cars = cur.fetchall()
        if not cars:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return cars


@router.get("/book-car")
def book_car():
    ...


@router.post("/payment")
def add_car_payment():
    ...


@router.get("/booking")
def list_today_booking(db: Connection = Depends(get_db)):
    with db.cursor() as cur:
        cur.execute("select * from bookings")
        bookings = cur.fetchall()
        if not bookings:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return bookings
