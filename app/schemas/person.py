from typing import Optional
from pydantic import BaseModel, EmailStr, Field, UUID4


class PersonBase(BaseModel):
    display_name: str = Field(..., max_length=36)
    email: EmailStr
    phone_number: Optional[int]

    class Config:
        orm_mode = True

class PersonInDb(PersonBase):
    id: UUID4

class PersonCreate(PersonBase):
    ...

class PersonUpdate(BaseModel):
    display_name: str = Field(..., max_length=36)
    email: EmailStr

class PersonInfo(PersonBase):
    ...
