from enum import Enum
from pydantic import BaseModel, Field, EmailStr, constr, root_validator


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

    # @root_validator
    # def check_passwords_match(cls, values):
    #     password, confirm_password = values.get("password"), values.get(
    #         "confirm_password"
    #     )
    #     if (
    #         password is not None
    #         and confirm_password is not None
    #         and password != confirm_password
    #     ):
    #         raise ValueError("passwords do not match")
    #     return values


class RegisterCustomerSchema(BaseRegisterSchema):
    type: str = UserType.customer


class RegisterEmployeeSchema(BaseModel):
    type: str = UserType.employee
