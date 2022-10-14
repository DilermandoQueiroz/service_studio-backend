from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.models import ServiceProvider
from app.schemas import ServiceProviderCreate, ServiceProviderInDBBase


class CRUDServiceProvider(CRUDBase[ServiceProvider, ServiceProviderCreate, ServiceProviderInDBBase]):
    
    def get_by_cpf(self, db: Session, cpf: str) -> Optional[ServiceProviderInDBBase]:
        return db.query(self.model).filter(self.model.cpf == cpf).first()


provider = CRUDServiceProvider(ServiceProvider)