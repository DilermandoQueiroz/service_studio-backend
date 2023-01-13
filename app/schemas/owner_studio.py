from typing import Type
from pydantic import BaseModel

class OwnerStudioCreate(BaseModel):
    person_id: str
    studio_id: str

    class Config:
        orm_mode = True

class OwnerStudioUpdate(BaseModel):
    person_id: str
    studio_id: str

    class Config:
        orm_mode = True
