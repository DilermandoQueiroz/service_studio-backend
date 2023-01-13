from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import Person, Studio
from app.schemas import PersonCreate, PersonUpdate


class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):
    ...


person = CRUDPerson(Person)