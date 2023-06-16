from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class UserType(str, Enum):
    customer = "CUSTOMER"
    employee = "EMPLOYEE"


class BaseUser(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=32)
    email: EmailStr
    first_name: str = Field(..., min_length=3, max_length=32)
    last_name: str = Field(..., min_length=3, max_length=32)
