from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.models import Studio
from app.schemas import StudioCreate, StudioUpdate


class CRUDStudio(CRUDBase[Studio, StudioCreate, StudioUpdate]):
    
    def get_by_email_studio(self, db: Session, email: str):
        return db.query(self.model).filter(self.model.email_studio == email).first()


studio = CRUDStudio(Studio)