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
    def validator_cpf(cls, numbers):
        cpf = [int(char) for char in numbers if char.isdigit()]

        if len(cpf) != 11:
            return ValueError("CPF do not match")

        if cpf == cpf[::-1]:
            return ValueError("CPF do not match")


        for i in range(9, 11):
            value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                return ValueError("CPF do not match")

        return numbers

class ClientInDBBase(ClientCreate):
    id: int
    email: str