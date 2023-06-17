import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from psycopg import Connection

from app.db import get_db
from app import oauth
from app.schemas.cars_schemas import BookingInSchema, CarSchema, BookingPaymentIn

import pytz

router = APIRouter(prefix="/cars", tags=["cars"])


@router.get("/")
def list_available_cars(
    db: Connection = Depends(get_db), auth_user=Depends(oauth.get_current_user)
) -> list[CarSchema]:
    with db.cursor() as cur:
        cur.execute("SELECT * FROM cars WHERE is_available = true")
        cars = cur.fetchall()
        if not cars:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return cars


@router.get("/{car_id}/book")
def book_car(
    booking: BookingInSchema,
    car_id: int,
    db: Connection = Depends(get_db),
    auth_user=Depends(oauth.get_current_user),
):
    if (booking.hire_date >= datetime.datetime.now(tz=pytz.UTC)) and (
        booking.hire_date < booking.return_date
    ):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Enter correct date"
        )
    with db.cursor() as cur:
        cur.execute(
            """
                select count(*) as user_booking_count from bookings where auth_user=%s;
            """,
            (auth_user.get("id"),),
        )
        count = cur.fetchone().get("user_booking_count")
        if count >= 7:
            raise HTTPException(
                status_code=406, detail="Customer not can not book more than 7 times."
            )
    with db.cursor() as cur:
        cur.execute(
            "INSERT INTO bookings (car, auth_user, hire_date, return_date) VALUES (%s, %s, %s, %s) RETURNING *",
            (car_id, auth_user.get("id"), booking.hire_date, booking.return_date),
        )
        db_booking = cur.fetchone()
        db.commit()

    return db_booking


@router.post("/book/{booking_id}/payment")
def add_car_booking_payment(
    payment: BookingPaymentIn,
    booking_id: int,
    db: Connection = Depends(get_db),
    auth_user=Depends(oauth.get_current_user),
):
    with db.cursor() as cur:
        cur.execute(
            """
                INSERT INTO payments (booking, amount)
                VALUES (%s, %s) RETURNING *;
            """,
            (booking_id, payment.amount),
        )
        db_payment = cur.fetchone()
        print(db_payment)
    db.commit()
    return db_payment


@router.get("/booking")
def list_today_booking(
    db: Connection = Depends(get_db), auth_user=Depends(oauth.get_current_user)
):
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    next_day = today + datetime.timedelta(days=1)

    with db.cursor() as cur:
        cur.execute(
            """SELECT B.ID,
                U.USERNAME,
                U.FIRST_NAME,
                U.LAST_NAME,
                C.MODEL,
                C.TYPE,
                B.HIRE_DATE,
                B.RETURN_DATE
                FROM BOOKINGS AS B
                LEFT OUTER JOIN USERS AS U ON B.AUTH_USER = U.ID
                LEFT OUTER JOIN CARS AS C ON B.CAR = C.ID 
                WHERE hire_date >= %s AND hire_date <= %s""",
            (today, next_day),
        )
        bookings = cur.fetchall()
        if not bookings:
            return []
    return bookings
