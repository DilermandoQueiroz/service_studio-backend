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

@router.post("/create", response_model=schemas.SellCreate, status_code = status.HTTP_201_CREATED) #dependencies=[Depends(validate_token_client)])
def create_sell(sell: schemas.SellCreateApi, db: Session = Depends(get_db), user = Depends(validate_token_client)):
    try:
        db_service_provider = crud.provider.get_by_id(db=db, id=user["user_id"])
        db_client = crud.person.get_by_email(db=db, email=sell.client_email)
        exceptions = []
        if sell.studio_id:
            db_studio = crud.studio.get_by_id(db=db, id=sell.studio_id)

            if not db_studio:
                exceptions.append("studio")

        if not db_service_provider:
            exceptions.append("service provider")
        if not db_client:
            exceptions.append("client")

        if len(exceptions) > 0:
            raise HTTPException(status_code=404, detail=f"{', '.join(exceptions)} not exists")
       
        sell_in = schemas.SellCreate(
            studio_id = sell.studio_id,
            client_id = db_client.id,
            service_provider_id = user["user_id"],
            price = sell.price,
            start_time = sell.start_time,
            actual_session = sell.actual_session,
            scheduled_time = sell.scheduled_time,
            description = sell.description,
            finished = sell.finished
        )

        return crud.sell.create(db=db, obj_in=sell_in)
    except Exception as error:
        logger.error(error)
        raise error

@router.put("/update")
def update_sell_by_id(sell_in: schemas.SellUpdate, db: Session = Depends(get_db)):
    sell = crud.sell.get_by_id(db=db, id=sell_in.id)
    if not sell:
        raise HTTPException(status_code=404, detail="Sell not found")
    sell = crud.sell.update(db=db, db_obj=sell, obj_in=sell_in)
    return sell

@router.delete("/remove")
def remove_sell_by_id(id: str = None, db: Session = Depends(get_db)):
    response = crud.sell.remove_by_id(db=db, id=id)

    if not response:
        raise HTTPException(status_code=400, detail="Id not exists")
    
    return response

@router.get("/all", response_model=List[schemas.SellInDBBase])
def read_sells(db: Session = Depends(get_db)):
    return crud.sell.get_all(db)
