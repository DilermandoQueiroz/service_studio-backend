from typing import Optional

from pydantic import BaseModel, validator, EmailStr, Field

class ServiceProviderCreate(BaseModel):
    name: str = Field(..., max_length=36)
    display_name: str = Field(..., max_length=36)
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

class ServiceProviderInDBBase(ServiceProviderCreate):
    id: int
    email: str