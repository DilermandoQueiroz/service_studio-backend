from typing import List

import app.crud as crud
import app.schemas as schemas
from app.custom_logger import custom_logger
from .dependencies import get_db, validate_token_client
from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.firebase_utils import validate_token
from sqlalchemy.orm import Session

logger = custom_logger(__name__)

router = APIRouter(
    prefix="/sell",
    tags=["Sell"],
)

@router.post("/create", response_model=schemas.SellCreate, status_code = status.HTTP_201_CREATED, dependencies=[Depends(validate_token_client)])
def create_sell(sell: schemas.SellCreate, db: Session = Depends(get_db)):
    try:
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
