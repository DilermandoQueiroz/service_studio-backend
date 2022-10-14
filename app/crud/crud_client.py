from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.models import Client
from app.schemas import ClientCreate, ClientInDBBase


class CRUDClient(CRUDBase[Client, ClientCreate, ClientInDBBase]):

    def get_by_cpf(self, db: Session, cpf: str) -> Optional[ClientInDBBase]:
        return db.query(self.model).filter(self.model.cpf == cpf).first()


client = CRUDClient(Client)