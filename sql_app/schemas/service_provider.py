from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class BaseServiceProvider(BaseModel):
    # TODO: validate phone number E.164
    display_name: str = Field(..., max_length=36)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)

class ServiceProviderFireBase(BaseServiceProvider):
    password: str

class ServiceProviderCreate(BaseServiceProvider):
    birth_date: date
    cpf: str = Field(..., max_length=11)
    name: str = Field(..., max_length=36)
    description: Optional[str] = Field(None, max_length=255)

    class Config:
        orm_mode = True

    # @validator("cpf")
    # def validator_cpf(cls, numbers):
    #     cpf = [int(char) for char in numbers if char.isdigit()]

    #     if len(cpf) != 11:
    #         return ValueError("CPF do not match")

    #     if cpf == cpf[::-1]:
    #         return ValueError("CPF do not match")

    #     for i in range(9, 11):
    #         value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
    #         digit = ((value * 10) % 11) % 10
    #         if digit != cpf[i]:
    #             return ValueError("CPF do not match")

    #     return numbers

class ServiceProviderInDBBase(ServiceProviderCreate):
    id: int
    email: str

class ServiceProviderAll(BaseModel):
    birth_date: date
    display_name: str = Field(..., max_length=36)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    password: str
    cpf: str = Field(..., max_length=11)
    description: Optional[str] = Field(None, max_length=255)