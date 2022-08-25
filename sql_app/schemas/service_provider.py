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

    @validator("cpf")
    def validator_cpf(cls, v):
        # TODO: validate cpf
        return v

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
