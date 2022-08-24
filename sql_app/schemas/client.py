from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, validator, EmailStr, Field

class ClientCreate(BaseModel):
    name: str = Field(..., max_length=36)
    display_name: str = Field(..., max_length=36)
    birth_date: date
    cpf: str = Field(..., max_length=11)
    country: Optional[str] = Field(None, max_length=3, min_length=2) 
    state: Optional[str] = Field(None, max_length=2)
    city: Optional[str] = Field(None, max_length=32)
    district: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=100)
    number: Optional[int] = Field(0, ge=0)
    zip_code: Optional[str] = Field(None, max_length=10)
    complement: Optional[str] = Field(None, max_length=15) 
    email: EmailStr
    phone_number: Union[str, None] = Field(None, max_length=20)

    class Config:
        orm_mode = True

    @validator("cpf")
    def validator_cpf(cls, v):
        # TODO: validate cpf
        return v

class ClientInDBBase(ClientCreate):
    id: int
    email: str