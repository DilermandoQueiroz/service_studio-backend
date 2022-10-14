from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

class SellCreate(BaseModel):
    studio_name: Optional[str] = Field(None, max_length=36)
    client_name: str = Field(..., max_length=36)
    service_provider_name: str = Field(..., max_length=36)
    service_style_name: Optional[str] = Field(None, max_length=36)
    tender_id: Optional[int] = Field(None, ge=0)
    price: float = Field(0.0, ge=0.0)
    studio_rate: Optional[int] = Field(0, ge=0, le=5)
    client_rate: Optional[int] = None
    service_provider_rate: Optional[int] = None
    client_suggestion_desc: Optional[str] = Field(None, max_length=140)
    number_of_sessions: Optional[int] = Field(1, ge=1)
    client_contract_confirmed: Optional[bool] = None
    service_provider_contract_confirmed: Optional[bool] = None
    start_time: datetime
    last_update: Optional[datetime] = None
    finish_time: Optional[datetime] = None 
    description: Optional[str] = Field(None, max_length=255)
    
    class Config:
        orm_mode = True

class SellInDBBase(SellCreate):
    id: int
    