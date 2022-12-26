import sys
from fastapi import Depends

sys.path += [
    "/Users/dilermando/dev/service_studio-backend/"
]

from sqlalchemy.orm import Session

import app.crud as crud
import app.schemas as schemas
from app.routers.dependencies import get_db
from app.tests.utils import random_lower_string, random_email

name = random_lower_string()
email = random_email()

def test_create_person(db: Session = Depends(get_db)) -> None:
    person_in = schemas.person.PersonCreate(display_name=name, email=email)
    person = crud.person.create(db=db, obj_in=person_in)

    assert person.display_name == name
    assert person.email == email