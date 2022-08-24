from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from models import Client
from schemas import ClientCreate, ClientInDBBase


class CRUDItem(CRUDBase[Client, ClientCreate, ClientInDBBase]):

    def get_by_cpf(self, db: Session, cpf: str) -> Optional[ClientInDBBase]:
        return db.query(self.model).filter(self.model.cpf == cpf).first()


client = CRUDItem(Client)