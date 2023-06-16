from enum import Enum
from pydantic import BaseModel, Field, EmailStr


class UserType(str, Enum):
    customer = "CUSTOMER"
    employee = "EMPLOYEE"


class BaseRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    email: EmailStr
    first_name: str = Field(..., min_length=3, max_length=32)
    last_name: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=6, max_length=64)
    confirm_password: str = Field(..., min_length=6, max_length=64)


class RegisterCustomerSchema(BaseRegisterSchema):
    type: str = UserType.customer


class RegisterEmployeeSchema(BaseModel):
    type: str = UserType.employee
