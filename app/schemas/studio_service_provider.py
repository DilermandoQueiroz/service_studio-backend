from typing import Optional, Type
from pydantic import UUID4, BaseModel, EmailStr, Field

class CreateStudioServiceProvider(BaseModel):
    service_provider_id: UUID4
    studio_id: UUID4
    comission: Optional[float] = Field(0.0, ge=0.0)
    studio_accept: Optional[bool] = False
    service_provider_accept: Optional[bool] = False

    class Config:
        orm_mode = True

class UpdateStudioServiceProvider(BaseModel):
    comission: Optional[float] = Field(0.0, ge=0.0)
    studio_accept: Optional[bool] = False
    service_provider_accept: Optional[bool] = False

    class Config:
        orm_mode = True

class RequestServiceProvider(BaseModel):
    email_studio: EmailStr

    class Config:
        orm_mode = True

class RequestStudio(BaseModel):
    email_service_provider: EmailStr

    class Config:
        orm_mode = True