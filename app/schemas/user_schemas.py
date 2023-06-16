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
    type: str


class UserIn(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=6, max_length=64)


class Token(BaseModel):
    access_token: str
    toke_type: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    type: str
    # token: Token


class TokenData(BaseModel):
    id: int
    email: EmailStr
