from typing import Optional

from pydantic import BaseModel, EmailStr, Field

class StudioCreate(BaseModel):
    id: str = Field(..., max_length=36)
    studio_name: str = Field(..., max_length=36)
    country: Optional[str] = Field(None, max_length=3, min_length=2) 
    state: Optional[str] = Field(None, max_length=2)
    city: Optional[str] = Field(None, max_length=32)
    district: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = Field(None, max_length=100)
    number: Optional[int] = Field(0, ge=0)
    zip_code: Optional[str] = Field(None, max_length=10)
    complement: Optional[str] = Field(None, max_length=15)
    email_studio: Optional[EmailStr] = None
    description: Optional[str] = Field(None, max_length=255)

    class Config:
        orm_mode = True

class StudioUpdate(BaseModel):
    ...

class StudioInDb(StudioCreate):
    id: str = Field(..., max_length=36)

    class Config:
        orm_mode = True