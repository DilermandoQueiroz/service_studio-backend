from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from db import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Args:
            ModelType: A SQLAlchemy model class
            CreateSchemaType: A Pydantic model (schema) class for create
            UpdateSchemaType: A Pydantic model (schema) class for update
        """
        self.model = model

    def get_by_email_list(self, db: Session, emails: list) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.email.in_(emails)).all()

    def get_by_email(self, db: Session, email: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_by_provider_email(self, db: Session, email: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_by_name(self, db: Session, name: str) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.name == name).first()
    
    def get_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove_by_name(self, db: Session, *, name: str) -> ModelType:
        obj = self.get_by_name(db=db, name=name)
        
        if obj:
            db.delete(obj)
            db.commit()

        return obj