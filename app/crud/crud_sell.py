import email
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.models import Sell
from app.schemas import SellCreate, SellInDBBase


class CRUDSell(CRUDBase[Sell, SellCreate, SellInDBBase]):
    ...

    def get_clients_unique_by_provider_email(self, db: Session, service_provider_email: str) -> Optional[SellInDBBase]:
        sells = db.query(self.model).filter(self.model.service_provider_name == service_provider_email).distinct(self.model.client_name).all()
        clients_email = []

        for sell in sells:
            clients_email.append(sell.client_name)

        return clients_email

    def get_by_provider_email(self, db: Session, service_provider_email: str) -> Optional[SellInDBBase]:
        return db.query(self.model).filter(self.model.service_provider_name == service_provider_email).all()

    def delete_sell_by_email_service_provider(self, db: Session, service_provider_email: str):
        sells = self.get_by_provider_email(db=db, service_provider_email=service_provider_email)

        if sells:
            for sell in sells:
                db.delete(sell)
                db.commit()

        return sells

sell = CRUDSell(Sell)