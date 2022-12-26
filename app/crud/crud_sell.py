import email
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.models import Sell
from app.schemas import SellCreate, SellInDBBase, SellUpdate


class CRUDSell(CRUDBase[Sell, SellCreate, SellUpdate]):

    def get_by_provider_email(self, db: Session, id: str) -> Optional[SellInDBBase]:
        return db.query(self.model).filter(self.model.service_provider_id == id).all()

sell = CRUDSell(Sell)