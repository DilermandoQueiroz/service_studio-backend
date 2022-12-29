import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.models import Sell, Person
from app.schemas import SellCreate, SellInDBBase, SellUpdate, SellInfo


class CRUDSell(CRUDBase[Sell, SellCreate, SellUpdate]):

    def get_by_provider_id(self, db: Session, id: str) -> SellInfo:
        return db.query(
            self.model,
            Person.display_name, Person.email
            ).join(Person.sell).filter(self.model.service_provider_id == id).all()
    
    def get_next_sells(self, db: Session, id: str) -> SellInfo:
        current_time = datetime.datetime.utcnow()

        return db.query(
            self.model,
            Person.display_name,
            Person.email
            ).join(Person.sell).filter(
                self.model.service_provider_id == id,
                self.model.finished == False,
                self.model.scheduled_time > current_time
            ).first()

sell = CRUDSell(Sell)