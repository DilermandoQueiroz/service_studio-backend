from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import StudioServiceProvider, ServiceProvider, Studio, Person
from app.schemas import CreateStudioServiceProvider, UpdateStudioServiceProvider

class CRUDStudioServiceProvider(CRUDBase[StudioServiceProvider, CreateStudioServiceProvider,
                                 UpdateStudioServiceProvider]):
    
    def get_by_service_provider(self, service_provider_id: str, db: Session):
        return db.query(self.model, Studio).join(self.model.studio).\
            filter(self.model.service_provider_id == service_provider_id).all()

    def get_by_studio(self, studio_id: str, db: Session):
        return db.query(self.model, Person).join(self.model.service_provider).\
            join(ServiceProvider.person).filter(self.model.studio_id == studio_id).all()

    def has_connection(self, studio_id: str, service_provider_id: str, db: Session):
        connection = db.query(self.model, Person)\
            .filter(self.model.studio_id == studio_id,
                    self.model.service_provider_id == service_provider_id,
                    self.model.studio_accept == True,
                    self.model.service_provider_accept == True).first()
        return connection

studio_service_provider = CRUDStudioServiceProvider(StudioServiceProvider)