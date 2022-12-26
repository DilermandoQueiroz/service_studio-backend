from typing import List, Optional

from .base import CRUDBase
from app.models import ServiceProvider, Person, Sell
from app.schemas import ServiceProviderCreate, ServiceProviderUpdate, PersonInfo
from sqlalchemy.orm import Session

class CRUDServiceProvider(CRUDBase[ServiceProvider, ServiceProviderCreate, ServiceProviderUpdate]):
    
    def get_by_email(self, db: Session, email: str) -> Optional[ServiceProvider]:
        return db.query(self.model, Person).join(Person).filter(Person.email == email).all()

    def remove_by_email(self, db: Session, email: str) -> ServiceProvider:
        test = self.get_by_email(db=db, email=email)
        if test:
            db.delete(test)
            db.commit()

        return test

    def get_clients(self, db: Session, id: str) -> List[PersonInfo]:
        return db.query(Sell.client_id, Person.email, Person.display_name).join(Person.sell)\
                .filter(Sell.service_provider_id == id).distinct().all()


provider = CRUDServiceProvider(ServiceProvider)