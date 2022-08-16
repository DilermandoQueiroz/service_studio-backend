from datetime import date, datetime
from typing import Union

from pydantic import BaseModel, validator, EmailStr, Field

class StudioCreate(BaseModel):
    name: str = Field(..., max_length=32)
    display_name: str = Field(..., max_length=32)
    country: Union[str, None] = Field(None, max_length=3, min_length=2) 
    state: Union[str, None] = Field(None, max_length=2)
    city: Union[str, None] = Field(None, max_length=32)
    district: Union[str, None] = Field(None, max_length=100)
    address: Union[str, None] = Field(None, max_length=100)
    number: Union[int, None] = Field(0, ge=0)
    zip_code: Union[str, None] = Field(None, max_length=10)
    complement: Union[str, None] = Field(None, max_length=15)
    email: Union[EmailStr , None] = None
    phone_number: Union[str, None] = Field(None, max_length=20)
    description: Union[str, None] = Field(None, max_length=255)
    email_owner: Union[EmailStr, None] = None

    class Config:
        orm_mode = True

class Studio(StudioCreate):
    id: int
    email: Union[str , None] = None
    email_owner: Union[str, None] = None

    class Config:
        orm_mode = True

class ServiceProviderCreate(BaseModel):
    name: str = Field(..., max_length=32)
    display_name: str = Field(..., max_length=32)
    cpf: str = Field(..., max_length=11)
    email: Union[EmailStr, None] = None
    phone_number: Union[str, None] = Field(None, max_length=20)
    signal: Union[int, None] = Field(None, ge=0)
    description: Union[str, None] = Field(None, max_length=255)

    class Config:
        orm_mode = True
    
    @validator("cpf")
    def validator_cpf(cls, v):
        # TODO: validate cpf
        return v

class ServiceProvider(ServiceProviderCreate):
    id: int
    email: Union[str, None] = None

    class Config:
        orm_mode = True

class ClientCreate(BaseModel):
    name: str = Field(..., max_length=32)
    display_name: str = Field(..., max_length=32)
    birth_date: date
    cpf: str = Field(..., max_length=11)
    country: Union[str, None] = Field(None, max_length=3, min_length=2) 
    state: Union[str, None] = Field(None, max_length=2)
    city: Union[str, None] = Field(None, max_length=32)
    district: Union[str, None] = Field(None, max_length=100)
    address: Union[str, None] = Field(None, max_length=100)
    number: Union[int, None] = Field(0, ge=0)
    zip_code: Union[str, None] = Field(None, max_length=10)
    complement: Union[str, None] = Field(None, max_length=15) 
    email: Union[EmailStr, None] = None 
    phone_number: Union[str, None] = Field(None, max_length=20)

    class Config:
        orm_mode = True

    @validator("cpf")
    def validator_cpf(cls, v):
        # TODO: validate cpf
        return v

class Client(ClientCreate):
    id: int
    email: Union[str, None] = None 

    class Config:
        orm_mode = True

class SellCreate(BaseModel):
    studio_name: Union[str, None] = Field(None, max_length=32)
    client_name: str = Field(..., max_length=32)
    service_provider_name: str = Field(..., max_length=32)
    service_style_name: Union[str, None] = Field(None, max_length=32)
    tender_id: Union[int, None] = Field(None, ge=0)
    price: float = Field(0.0, ge=0.0)
    studio_rate: Union[int, None] = None
    client_rate: Union[int, None] = None
    service_provider_rate: Union[int, None] = None
    client_suggestion_desc: Union[str, None] = Field(None, max_length=140)
    client_satisfied: Union[bool, None] = None
    number_of_sessions: int = Field(1, ge=1)
    client_contract_confirmed: Union[bool, None] = None
    service_provider_contract_confirmed: Union[bool, None] = None
    start_time: datetime
    last_update: Union[datetime, None] = None
    finish_time: Union[datetime, None] = None 

    class Config:
        orm_mode = True

class Sell(SellCreate):
    id: int
    
    class Config:
        orm_mode = True