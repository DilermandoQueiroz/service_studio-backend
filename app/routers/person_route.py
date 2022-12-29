from typing import List

import app.crud as crud
import app.schemas as schemas
from .dependencies import get_db, validate_token_client
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.custom_logger import custom_logger

logger = custom_logger(__name__)

router = APIRouter(
    prefix="/person",
    tags=["Person"],
)

@router.post("/create", response_model = schemas.PersonCreate, status_code = status.HTTP_201_CREATED)
def create_person(person: schemas.PersonCreate, db: Session = Depends(get_db)):
    try:
        db_person_email = crud.person.get_by_email(db=db, email=person.email)
        exceptions = []
        
        if db_person_email:
            exceptions.append("email")

        if len(exceptions) > 0:
            raise HTTPException(status_code=422, detail=f"{', '.join(exceptions)} already registered")

        return crud.person.create(db=db, obj_in=person)
    except Exception as error:
        logger.error(error)
        raise error

@router.get("/all", response_model=List[schemas.PersonInDb])
def read_persons(db: Session = Depends(get_db)):
    return crud.person.get_all(db)

@router.get("/remove")
def remove_person_by_email(email: str = None, db: Session = Depends(get_db)):
    response = crud.person.remove_by_email(db=db, email=email)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return response

@router.get("/", response_model=schemas.PersonInfo, dependencies=[Depends(validate_token_client)])
def get_person_name_by_email(email: str = None, db: Session = Depends(get_db)):
    db_person_email = crud.person.get_by_email(db=db, email=email)

    if db_person_email:
        return schemas.PersonInfo(display_name=db_person_email.display_name, email=email)
    else:
        raise HTTPException(status_code=400, detail="This user not exist")
