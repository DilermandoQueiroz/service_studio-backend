from typing import List

import app.crud as crud
import app.schemas as schemas
from app.custom_logger import custom_logger
from .dependencies import get_db, validate_token_client
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.firebase_utils import (create_service_provider_firebase,
                            delete_by_user_uid, get_user_by_email, validate_token)
from sqlalchemy.orm import Session

logger = custom_logger(__name__)

router = APIRouter(
    prefix="/provider",
    tags=["Service Provider"],
)

@router.post("/create", status_code = status.HTTP_201_CREATED)
def create_service_provider(service_provider: schemas.ServiceProviderCreateFirebase, db: Session = Depends(get_db)):
    user = False
    try:
        if crud.provider.get_by_email(db=db, email=service_provider.email):
            raise HTTPException(status_code=422, detail=f"Provider already registered")

        user = get_user_by_email(service_provider.email)

        if not user:
            user = create_service_provider_firebase(service_provider)
        
        if user:
            db_service_provider_id = crud.provider.get_by_id(db=db, id=user.uid)

            if db_service_provider_id:
                raise HTTPException(status_code=422, detail=f"Provider already registered")

            person = crud.person.get_by_email(db=db, email=service_provider.email)

            if person:
                person_db = person
            else:
                person = schemas.PersonCreate(
                    display_name=service_provider.display_name,
                    email=service_provider.email
                )
                
                person_db = crud.person.create(db=db, obj_in=person)
            
            user_db = schemas.ServiceProviderCreate(
                id=user.uid,
                person_id=person_db.id
            )

            crud.provider.create(db=db, obj_in=user_db)

            return "ok"
            
    except Exception as error:
        logger.error(error)
        raise error
    finally:
        if user:
            db_service_provider_name = crud.provider.get_by_id(db=db, id=user.uid)
            if not db_service_provider_name:
                delete_by_user_uid(user.uid)

@router.get("/remove")
def remove_service_provider_by_email(db: Session = Depends(get_db), user = Depends(validate_token_client)):
    try:
        crud.sell.delete_sell_by_email_service_provider(db=db, service_provider_email=user["email"])
        response = crud.person.remove_by_email(db=db, email=user["email"])

        if not response:
            raise HTTPException(status_code=400, detail="Email not exists")
        
        delete_by_user_uid(user["user_id"])

        return response
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/all")
def read_service_providers(db: Session = Depends(get_db)):
    return crud.provider.get_all(db)

@router.get("/clients", response_model=List[schemas.PersonInfo])
def get_provider_clients(db: Session = Depends(get_db), user = Depends(validate_token_client)):
    return crud.provider.get_clients(db=db, id=user["user_id"])

@router.get("/sells")
def get_provider_sells(db: Session = Depends(get_db), user = Depends(validate_token_client)):
    return crud.sell.get_by_provider_id(db=db, id=user["user_id"])
