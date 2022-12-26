from pydantic import BaseModel, EmailStr, Field, UUID4


class PersonBase(BaseModel):
    display_name: str = Field(..., max_length=36)
    email: EmailStr

    class Config:
        orm_mode = True

class PersonInDb(PersonBase):
    id: UUID4

class PersonCreate(PersonBase):
    ...

class PersonUpdate(BaseModel):
    display_name: str = Field(..., max_length=36)
    email: EmailStr

class PersonInfo(BaseModel):
    display_name: str = Field(..., max_length=36)
    email: EmailStr
