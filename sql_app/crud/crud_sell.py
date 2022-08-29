from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from models import Sell
from schemas import SellCreate, SellInDBBase


class CRUDSell(CRUDBase[Sell, SellCreate, SellInDBBase]):
    ...

    def get_by_provider_email(self, db: Session, service_provider_email: str) -> Optional[SellInDBBase]:
        return db.query(self.model).filter(self.model.service_provider_name == service_provider_email).all()

sell = CRUDSell(Sell)