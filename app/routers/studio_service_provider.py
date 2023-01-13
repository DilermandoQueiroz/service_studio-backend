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
    prefix="/link",
    tags=["StudioServiceProvider"],
)

@router.post("/request/provider")
def link_studio_service_provider_by_provider(request: schemas.RequestServiceProvider, db: Session = Depends(get_db), user = Depends(validate_token_client)):
    studio = crud.studio.get_by_email_studio(db=db, email=request.email_studio)
    link = schemas.CreateStudioServiceProvider(
        service_provider_id=user["service_provider_id"],
        studio_id=studio.id,
        service_provider_accept=True
    )
    return crud.studio_service_provider.create(db=db, obj_in=link)

@router.post("/request/studio")
def link_studio_service_provider_by_studio(request: schemas.RequestStudio, db: Session = Depends(get_db), user = Depends(validate_token_client)):
    # TODO
    ...

@router.get("/provider")
def service_provider_has_studio(user = Depends(validate_token_client), db = Depends(get_db)):
    return crud.studio_service_provider.get_by_service_provider(db=db, service_provider_id=user["service_provider_id"])

@router.get("/studio")
def studio_has_service_provider(studio_id = Depends(is_owner_studio), db=Depends(get_db)):
    return crud.studio_service_provider.get_by_studio(studio_id=studio_id, db=db)

@router.put("/{id}")
def update_link(link: schemas.UpdateStudioServiceProvider, id: str, db=Depends(get_db)):
    # TODO: vulnerability! confirm if it is the studio or service provider
    # that request this in the link_db 
    print(link)
    link_db = crud.studio_service_provider.get_by_id(id=id, db=db)

    if not link_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return crud.studio_service_provider.update(db=db, db_obj=link_db, obj_in=link)

@router.delete("/{id}")
def delete_link(id: str, db=Depends(get_db)):
    # TODO: vulnerability! confirm if it is the studio or service provider
    # that request this in the link_db
    
    # link = crud.studio_service_provider.get_by_id(db=db, id=id)
    
    # if not link:
    #     raise HTTPException(status_code=400, detail="Id not exists")

    return crud.studio_service_provider.remove_by_id(db=db, id=id)

@router.get("/all")
def read_studios(db: Session = Depends(get_db)):
    return crud.studio_service_provider.get_all(db)