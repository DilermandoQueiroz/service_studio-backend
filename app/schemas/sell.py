from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field

class SellBasic(BaseModel):
    studio_id: Optional[str] = Field(None, max_length=36)
    
    price: float = Field(0.0, ge=0.0)
    start_time: datetime
    actual_session: Optional[int] = Field(1, ge=1)
    scheduled_time: Optional[datetime]
    description: Optional[str] = Field(None, max_length=255)
    finished: Optional[bool] = False

    class Config:
        orm_mode = True

class SellCreateApi(SellBasic):
    client_email: EmailStr

class SellCreate(SellBasic):
    client_id: UUID4
    service_provider_id: str = Field(..., max_length=36)

class SellUpdate(BaseModel):
    id: UUID4
    price: Optional[float] = Field(0.0, ge=0.0)
    actual_session: Optional[int] = Field(1, ge=1)
    scheduled_time: Optional[datetime]
    description: Optional[str] = Field(None, max_length=255)
    finished: Optional[bool] = None

class SellInDBBase(SellCreate):
    id: UUID4

class SellInfo(BaseModel):
    client_email: EmailStr
    price: float = Field(0.0, ge=0.0)
    start_time: datetime
    actual_session: Optional[int] = Field(1, ge=1)
    scheduled_time: Optional[datetime]
    description: Optional[str] = Field(None, max_length=255)
    finished: Optional[bool] = False
    