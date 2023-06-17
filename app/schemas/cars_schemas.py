from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class CarType(str, Enum):
    small_car = "SMALL_CAR"
    family_car = "FAMILY_CAR"
    van = "VAN"


class CarSchema(BaseModel):
    id: int
    company: int
    model: str
    type: CarType
    is_available: bool
    created_at: datetime


class BookingSchema(BaseModel):
    id: int
    car: int
    user: int
    hire_date: datetime
    return_date: datetime
    created_at: datetime


class BookingInSchema(BaseModel):
    hire_date: datetime
    return_date: datetime


class BookingOutSchema(BookingInSchema):
    id: int
    created_at: datetime
