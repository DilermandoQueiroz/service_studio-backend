from sqlalchemy.orm import Session
from .base import CRUDBase
from app.models import OwnerStudio, Person, Studio
from app.schemas import OwnerStudioCreate, OwnerStudioUpdate


class CRUDOwnerStudio(CRUDBase[OwnerStudio, OwnerStudioCreate, OwnerStudioUpdate]):
    
    def create(self, db: Session, *, person: Person, studio: Studio):
        
        owner_studio_obj = OwnerStudio(person=person, studio=studio)
        db.add(owner_studio_obj)
        db.commit()
        db.refresh(owner_studio_obj)
        return owner_studio_obj


owner_studio = CRUDOwnerStudio(OwnerStudio)