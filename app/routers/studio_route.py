from typing import List

import app.crud as crud
from app.firebase_utils import create_studio, get_user_by_uid
import app.schemas as schemas
from app.custom_logger import custom_logger
from .dependencies import get_db, validate_token_client, is_owner_studio
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

logger = custom_logger(__name__)

router = APIRouter(
    prefix="/studio",
    tags=["Studio"],
)

@router.post("/create", response_model = schemas.StudioCreate, status_code = status.HTTP_201_CREATED)
def create_studio_provider(studio: schemas.StudioCreate, db: Session = Depends(get_db), user = Depends(validate_token_client)):
    try:
        user_firebase = get_user_by_uid(uid=user["user_id"])

        if user_firebase.custom_claims.get('studio_id'):
            raise HTTPException(status_code=422, detail=f"Studio already registered")
        
        studio_db = crud.studio.create(db=db, obj_in=studio)
        
        create_studio(user["user_id"], studio_id=studio_db.id)
        
        person = crud.person.get_by_id(db=db, id=user["person_id"])
    
        crud.owner_studio.create(db=db, person=person, studio=studio_db)

        return studio_db
    except Exception as error:
        logger.error(error)
        raise error

@router.get("/remove")
def remove_studio_by_id(id: str = None, db: Session = Depends(get_db)):
    response = crud.studio.remove_by_id(db=db, id=id)

    if not response:
        raise HTTPException(status_code=400, detail="Studio not exists")
    
    return response

@router.get("/sells")
def get_sell_in_studio(db: Session = Depends(get_db), studio_id = Depends(is_owner_studio)):
    response = crud.sell.get_by_studio_id(db=db, id=studio_id)

    if not response:
        raise HTTPException(status_code=400, detail="Studio not exists")

    return response

@router.get("/all")
def read_studios(db: Session = Depends(get_db)):
    return crud.studio.get_all(db)

@router.get("/owner/all")
def read_studios(db: Session = Depends(get_db)):
    return crud.owner_studio.get_all(db)