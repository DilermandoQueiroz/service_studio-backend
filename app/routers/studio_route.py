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

# TODO: Create studio in firebase and database.
# @router.post("/create", response_model = schemas.StudioCreate, status_code = status.HTTP_201_CREATED)
# def create_studio_provider(request: Request, studio: schemas.StudioCreate, db: Session = Depends(get_db)):
#     try:
#         if validate_token(request.headers['authorization']):
#             db_studio_name = crud.studio.get_by_name(db=db, name=studio.name)
#             db_studio_owner_email = crud.studio.get_by_email(db=db, email=studio.email_owner)

#             if db_studio_name:
#                 raise HTTPException(status_code=400, detail="Name already registered")
#             elif db_studio_owner_email:
#                 raise HTTPException(status_code=400, detail="Owner email already registered")

#             return crud.studio.create(db=db, obj_in=studio)
#         else:
#             raise HTTPException(status_code=401, detail="Email not verified")
#     except Exception as error:
#         logger.error(error)
#         raise error

# TODO: validate token
# @router.get("/remove")
# def remove_studio_by_name(name: str = None, db: Session = Depends(get_db)):
#     response = crud.studio.remove_by_name(db=db, name=name)

#     if not response:
#         raise HTTPException(status_code=400, detail="Name not exists")
    
#     return response

@router.get("/all", response_model=List[schemas.StudioInDBBase])
def read_studios(db: Session = Depends(get_db)):
    return crud.studio.get_all(db)
