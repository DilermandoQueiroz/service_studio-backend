from typing import Optional, Union

from pydantic import BaseModel, EmailStr, Field

class StudioCreate(BaseModel):
    name: str = Field(..., max_length=36)
    display_name: str = Field(..., max_length=36)
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

class StudioInDBBase(StudioCreate):
    id: int
    email: Union[str , None] = None
    email_owner: str