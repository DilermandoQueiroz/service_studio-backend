from typing import List

import crud
import schemas
from custom_logger import custom_logger
from dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from firebase_utils import (create_service_provider_firebase,
                            delete_by_user_uid, validate_token)
from sqlalchemy.orm import Session

logger = custom_logger(__name__)

router = APIRouter(
    prefix="/provider",
    tags=["Service Provider"],
)

# TODO: validate token
# @router.get("/", response_model = schemas.ServiceProviderInDBBase)
# def read_service_provider_by(name: str = None, cpf: str = None, email: str = None, db: Session = Depends(get_db)):
#     db_service_provider = False

#     if name:
#         db_service_provider = crud.provider.get_by_name(db=db, name=name)
#     elif email:
#         db_service_provider = crud.provider.get_by_email(db=db, email=email)
#     elif cpf:
#         db_service_provider = crud.provider.get_by_cpf(db=db, cpf=cpf)

#     if not db_service_provider:
#         raise HTTPException(status_code=404, detail="Service provider not found")
    
#     return db_service_provider

@router.post("/create", response_model = schemas.ServiceProviderCreate, status_code = status.HTTP_201_CREATED)
def create_service_provider(service_provider: schemas.ServiceProviderAll, db: Session = Depends(get_db)):
    user = False
    try:
        user_firebase = schemas.ServiceProviderFireBase(
            display_name=service_provider.display_name,
            email=service_provider.email,
            password=service_provider.password,
            phone_number=service_provider.phone_number
        )
        user = create_service_provider_firebase(user_firebase)
        
        if user:
            db_service_provider_cpf = crud.provider.get_by_cpf(db=db, cpf=service_provider.cpf)
            db_service_provider_name = crud.provider.get_by_name(db=db, name=user.uid)
            db_service_provider_email = crud.provider.get_by_email(db=db, email=service_provider.email)
            exceptions = []

            if db_service_provider_name:
                exceptions.append("name")
            if db_service_provider_cpf:
                exceptions.append("cpf")
            if db_service_provider_email:
                exceptions.append("email")

            if exceptions:
                raise HTTPException(status_code=400, detail=f"{', '.join(exceptions)} already registered")

            user_db = schemas.ServiceProviderCreate(
                birth_date=service_provider.birth_date,
                name=user.uid,
                display_name=service_provider.display_name,
                email=service_provider.email,
                phone_number=service_provider.phone_number,
                cpf=service_provider.cpf
            )

            return crud.provider.create(db=db, obj_in=user_db)
            
    except Exception as error:
        logger.error(error)
        raise error
    finally:
        if user:
            db_service_provider_name = crud.provider.get_by_name(db=db, name=user.uid)
            if not db_service_provider_name:
                delete_by_user_uid(user.uid)

@router.get("/remove")
def remove_service_provider_by_name(uid: str = None, db: Session = Depends(get_db)):
    try:
        response = crud.provider.remove_by_name(db=db, name=uid)
        print("passou")
        if not response:
            raise HTTPException(status_code=400, detail="Uid not exists")
        
        delete_by_user_uid(uid)

        return response
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/all", response_model=List[schemas.ServiceProviderInDBBase])
def read_service_providers(db: Session = Depends(get_db)):
    return crud.provider.get_all(db)

@router.get("/clients", response_model=List[schemas.ClientInDBBase])
def get_provider_clients(request: Request, db: Session = Depends(get_db)):
    user = validate_token(request.headers['authorization'])
    if user:
        db_clients_email = crud.sell.get_clients_unique_by_provider_email(db=db, service_provider_email=user["email"])
        if db_clients_email:
            db_clients = crud.client.get_by_email_list(db=db, emails=db_clients_email)
            return db_clients
        
        return db_clients_email

# TODO: For what?
# @app.get("/sell_by_email/", response_model=List[schemas.SellInDBBase])
# def sell_by_email(request: Request, db: Session = Depends(get_db)):
#     user = validate_token(request.headers['authorization'])
#     if user:
#         db_client = crud.sell.get_by_provider_email(db=db, service_provider_email=user['email'])
#         if db_client is None:
#             raise HTTPException(status_code=404, detail="Clients not found")
#         return db_client