from pydantic import UUID4, BaseModel, Field
from .person import PersonUpdate, PersonBase

class ServiceProviderCreate(BaseModel):
    id: str = Field(..., max_length=36)
    person_id: UUID4

class ServiceProviderCreateFirebase(PersonBase):
    password: str

class ServiceProviderInDb(ServiceProviderCreate):
    ...

class ServiceProviderUpdate(PersonUpdate):
    ...