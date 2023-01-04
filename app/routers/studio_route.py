from typing import List

import app.crud as crud
import app.schemas as schemas
from app.custom_logger import custom_logger
from .dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.firebase_utils import validate_token
from sqlalchemy.orm import Session

logger = custom_logger(__name__)

router = APIRouter(
    prefix="/studio",
    tags=["Studio"],
)

@router.post("/create", response_model = schemas.StudioCreate, status_code = status.HTTP_201_CREATED)
def create_studio_provider(studio: schemas.StudioCreate, db: Session = Depends(get_db)):
    try:
        db_studio = crud.studio.get_by_id(db=db, id=studio.id)

        if db_studio:
            raise HTTPException(status_code=422, detail=f"Studio already registered")

        return crud.studio.create(db=db, obj_in=studio)
    except Exception as error:
        logger.error(error)
        raise error

# TODO: validate token
# @router.get("/remove")
# def remove_studio_by_name(name: str = None, db: Session = Depends(get_db)):
#     response = crud.studio.remove_by_name(db=db, name=name)

#     if not response:
#         raise HTTPException(status_code=400, detail="Name not exists")
    
#     return response

@router.get("/all", response_model=List[schemas.StudioInDb])
def read_studios(db: Session = Depends(get_db)):
    return crud.studio.get_all(db)
