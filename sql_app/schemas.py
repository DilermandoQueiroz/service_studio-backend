from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel, validator, EmailStr, Field

class StudioCreate(BaseModel):
    name: str = Field(..., max_length=32)
    display_name: str = Field(..., max_length=32)
    country: Optional[str] = Field(None, max_length=3, min_length=2) 
    state: Optional[str] = Field(None, max_length=2)
    city: Optional[str] = Field(None, max_length=32)
    district: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=100)
    number: Optional[int] = Field(0, ge=0)
    zip_code: Optional[str] = Field(None, max_length=10)
    complement: Optional[str] = Field(None, max_length=15)
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = Field(None, max_length=20)
    description: Optional[str] = Field(None, max_length=255)
    email_owner: EmailStr

    class Config:
        orm_mode = True

class Studio(StudioCreate):
    id: int
    email: Union[str , None] = None
    email_owner: str

class ServiceProviderCreate(BaseModel):
    name: str = Field(..., max_length=32)
    display_name: str = Field(..., max_length=32)
    cpf: str = Field(..., max_length=11)
    email: EmailStr
    phone_number: Optional[str] = Field(None, max_length=20)
    signal: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=255)

    class Config:
        orm_mode = True
    
    @validator("cpf")
    def validator_cpf(cls, v):
        # TODO: validate cpf
        return v

class ServiceProvider(ServiceProviderCreate):
    id: int
    email: str

class ClientCreate(BaseModel):
    name: str = Field(..., max_length=32)
    display_name: str = Field(..., max_length=32)
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

class Client(ClientCreate):
    id: int
    email: str

class SellCreate(BaseModel):
    studio_name: Optional[str] = Field(None, max_length=32)
    client_name: str = Field(..., max_length=32)
    service_provider_name: str = Field(..., max_length=32)
    service_style_name: Optional[str] = Field(None, max_length=32)
    tender_id: Optional[int] = Field(None, ge=0)
    price: float = Field(0.0, ge=0.0)
    studio_rate: int = Field(0, ge=0, le=5)
    client_rate: Optional[int] = None
    service_provider_rate: Optional[int] = None
    client_suggestion_desc: Optional[str] = Field(None, max_length=140)
    client_satisfied: Optional[bool] = None
    number_of_sessions: int = Field(1, ge=1)
    client_contract_confirmed: Optional[bool] = None
    service_provider_contract_confirmed: Optional[bool] = None
    start_time: datetime
    last_update: Optional[datetime] = None
    finish_time: Optional[datetime] = None 

    class Config:
        orm_mode = True

class Sell(SellCreate):
    id: int