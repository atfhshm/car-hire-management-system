from fastapi import FastAPI

from dataclasses import dataclass

from .routes import auth, customers, cars

app = FastAPI()

app.include_router(auth.router)
app.include_router(customers.router)
app.include_router(cars.router)

from app.db import get_db


@app.on_event("startup")
def create_user():
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS users
                (
                    id serial NOT NULL,
                    username character varying(32) NOT NULL,
                    email character varying(32) NOT NULL,
                    first_name character varying(32) NOT NULL,
                    last_name character varying(32) NOT NULL,
                    type character varying(10) NOT NULL,
                    created_at timestamp with time zone NOT NULL DEFAULT NOW(),
                    is_active boolean NOT NULL DEFAULT true,
                    password character varying(128) NOT NULL,
                    PRIMARY KEY (id)
                );
            """
        )
        db.commit()


@app.on_event("startup")
def create_companies():
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS companies
                (
                    id serial NOT NULL,
                    name character varying(32) NOT NULL,
                    created_at timestamp with time zone DEFAULT NOW(),
                    PRIMARY KEY (id)
                );
            """
        )
        db.commit()


@app.on_event("startup")
def create_cars():
    db = get_db()
    with db.cursor() as cur:
        db.execute(
            """
                CREATE TABLE IF NOT EXISTS cars
                (
                    id serial NOT NULL,
                    company integer NOT NULL,
                    model character varying(64) NOT NULL,
                    type character varying(12) NOT NULL,
                    is_available boolean DEFAULT true,
                    created_at timestamp with time zone DEFAULT now(),
                    PRIMARY KEY (id),
                    CONSTRAINT car_company_fk FOREIGN KEY (company)
                        REFERENCES companies (id) MATCH SIMPLE
                        ON UPDATE NO ACTION
                        ON DELETE CASCADE
                        NOT VALID
                );
                """
        )
        db.commit()


@app.on_event("startup")
def create_bookings():
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            """    
                CREATE TABLE IF NOT EXISTS bookings
                (
                    id serial NOT NULL,
                    car integer NOT NULL,
                    auth_user integer NOT NULL,
                    hire_date timestamp with time zone NOT NULL DEFAULT NOW(),
                    return_date timestamp with time zone NOT NULL,
                    created_at timestamp with time zone DEFAULT Now(),
                    PRIMARY KEY (id),
                    CONSTRAINT booking_car_fk FOREIGN KEY (car)
                        REFERENCES cars (id) MATCH SIMPLE
                        ON UPDATE NO ACTION
                        ON DELETE CASCADE
                        NOT VALID,
                    CONSTRAINT booking_user_fk FOREIGN KEY (auth_user)
                        REFERENCES users (id) MATCH SIMPLE
                        ON UPDATE NO ACTION
                        ON DELETE CASCADE
                        NOT VALID
                );
                """
        )
        db.commit()


@app.on_event("startup")
def create_payments():
    db = get_db()
    with db.cursor() as cur:
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS payments
                (
                    id serial NOT NULL,
                    booking integer NOT NULL,
                    amount integer NOT NULL,
                    PRIMARY KEY (id),
                    CONSTRAINT payment_booking_fk FOREIGN KEY (booking)
                        REFERENCES bookings (id) MATCH SIMPLE
                        ON UPDATE NO ACTION
                        ON DELETE NO ACTION
                        NOT VALID
                );
                    """
        )
        db.commit()


@dataclass
class Message:
    project: str = "car-hire-management-system"
    location: str = "root"
    version: str = "0.0.1"


@app.get("/", tags=["root"], response_model=Message)
def root():
    return Message()
