from .base import CRUDBase
from app.models import Person
from app.schemas import PersonCreate, PersonUpdate


class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):
    ...


person = CRUDPerson(Person)