from typing import List

import crud
import schemas
from custom_logger import custom_logger
from .dependencies import get_db
from fastapi import APIRouter, Depends, HTTPException, Request, status
from firebase_utils import validate_token
from sqlalchemy.orm import Session

logger = custom_logger(__name__)

router = APIRouter(
    prefix="/sell",
    tags=["Sell"],
)

@router.post("/create", response_model=schemas.SellCreate, status_code = status.HTTP_201_CREATED)
def create_sell(request: Request, sell: schemas.SellCreate, db: Session = Depends(get_db)):
    try:
        if validate_token(request.headers['authorization']):
            db_service_provider = crud.provider.get_by_email(db=db, email=sell.service_provider_name)
            db_client = crud.client.get_by_email(db=db, email=sell.client_name)
            exceptions = []

            if sell.studio_name:
                db_studio = crud.studio.get_by_name(db=db, name=sell.studio_name)

                if not db_studio:
                    exceptions.append("studio")

            if not db_service_provider:
                exceptions.append("service provider")
            if not db_client:
                exceptions.append("client")

            if len(exceptions) > 0:
                print(exceptions)
                raise HTTPException(status_code=400, detail=f"{', '.join(exceptions)} not exists")

        return crud.sell.create(db=db, obj_in=sell)
    except Exception as error:
        logger.error(error)
        raise error

@router.get("/all", response_model=List[schemas.SellInDBBase])
def read_sells(db: Session = Depends(get_db)):
    return crud.sell.get_all(db)
