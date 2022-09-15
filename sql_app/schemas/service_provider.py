from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class BaseServiceProvider(BaseModel):
    display_name: str = Field(..., max_length=36)
    email: EmailStr

class ServiceProviderFireBase(BaseServiceProvider):
    password: str

class ServiceProviderDB(BaseServiceProvider):
    name: str = Field(..., max_length=36)

class ServiceProviderInDBBase(ServiceProviderDB):
    id: int
    name: str = Field(..., max_length=36)
    display_name: str = Field(..., max_length=36)
    email: EmailStr

class ServiceProviderCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: str = Field(..., max_length=36)