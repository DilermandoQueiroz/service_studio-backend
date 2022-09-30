from typing import List

import crud
import schemas
from .dependencies import get_db, validate_token_client
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from firebase_utils import validate_token
from custom_logger import custom_logger

logger = custom_logger(__name__)

router = APIRouter(
    prefix="/client",
    tags=["Client"],
)

# TODO: Validate token.
# @router.get("/", response_model=schemas.ClientInDBBase)
# def read_client_by_name(name: str = None, email: str = None, db: Session = Depends(get_db)):
#     if name:
#         db_client = crud.client.get_by_name(db=db, name=name)
#     elif email:
#         db_client = crud.client.get_by_email(db=db, email=email)
#     if db_client is None:
#         raise HTTPException(status_code=404, detail="Service provider not found")
    
#     return db_client

@router.post("/create", response_model = schemas.ClientCreate, status_code = status.HTTP_201_CREATED)
def create_client(request: Request, client: schemas.ClientCreate, db: Session = Depends(get_db)):
    try:
        user = validate_token(request.headers['authorization'])
        if user:
            db_client_cpf = crud.client.get_by_cpf(db=db, cpf=client.cpf)
            db_client_name = crud.client.get_by_name(db=db, name=client.name)
            db_client_email = crud.client.get_by_email(db=db, email=client.email)
            exceptions = []

            if db_client_name:
                exceptions.append("name")
            if db_client_cpf:
                exceptions.append("cpf")
            if db_client_email:
                exceptions.append("email")

            if len(exceptions) > 0:
                raise HTTPException(status_code=400, detail=f"{', '.join(exceptions)} already registered")

            return crud.client.create(db=db, obj_in=client)
        else:
            raise  HTTPException(status_code=400, detail="The code is not valid")
    except Exception as error:
        logger.error(error)
        print(error)

@router.get("/all", response_model=List[schemas.ClientInDBBase])
def read_clients(db: Session = Depends(get_db)):
    return crud.client.get_all(db)

@router.get("/remove")
def remove_client_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.client.remove_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return response

@router.get("/name", response_model=schemas.ClientShowSell, dependencies=[Depends(validate_token_client)])
def get_client_name_by_email(email: str = None, db: Session = Depends(get_db)):
    db_client_email = crud.client.get_by_email(db=db, email=email)

    if db_client_email:
        return schemas.ClientShowSell(display_name = db_client_email.display_name)
    else:
        raise HTTPException(status_code=400, detail="This user not exist")
