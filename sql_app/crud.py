from sqlalchemy.orm import Session

import models
import schemas


def create_studio(db: Session, studio: schemas.StudioCreate):
    db_studio = models.Studio(**studio.dict())
    db.add(db_studio)
    db.commit()
    db.refresh(db_studio)

    return db_studio


def create_service_provider(db: Session, service_provider: schemas.ServiceProviderCreate):
    db_service_provider = models.ServiceProvider(**service_provider.dict())
    db.add(db_service_provider)
    db.commit()
    db.refresh(db_service_provider)

    return db_service_provider


def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client


def create_sell(db: Session, sell: schemas.SellCreate):
    db_sell = models.Sell(**sell.dict())
    db.add(db_sell)
    db.commit()
    db.refresh(db_sell)

    return db_sell

# TODO: What is to return?


def delete_studio_by_name(db: Session, name: str):
    db_studio = get_studio_by_name(db=db, name=name)

    if db_studio:
        db.delete(db_studio)
        db.commit()

        return True

    return False

# TODO: What is to return?


def delete_service_provider_by_name(db: Session, name: str):
    db_service_provider = get_service_provider_by_name(db=db, name=name)

    if db_service_provider:
        db.delete(db_service_provider)
        db.commit()

        return True

    return False

# TODO: What is to return?


def delete_client_by_name(db: Session, name: str):
    db_service_provider = get_client_by_name(db=db, name=name)

    if db_service_provider:
        db.delete(db_service_provider)
        db.commit()

        return True

    return False


def get_studio(db: Session):
    return db.query(models.Studio).all()


def get_service_provider(db: Session):
    return db.query(models.ServiceProvider).all()


def get_client(db: Session):
    return db.query(models.Client).all()


def get_sell(db: Session):
    return db.query(models.Sell).all()


def get_studio_by_id(db: Session, id: int):
    return db.query(models.Studio).filter(models.Studio.id == id).first()


def get_service_provider_by_id(db: Session, id: int):
    return db.query(models.ServiceProvider).filter(models.ServiceProvider.id == id).first()


def get_client_by_id(db: Session, id: int):
    return db.query(models.Client).filter(models.Client.id == id).first()


def get_studio_by_name(db: Session, name: str):
    return db.query(models.Studio).filter(models.Studio.name == name).first()


def get_service_provider_by_name(db: Session, name: str):
    return db.query(models.ServiceProvider).filter(models.ServiceProvider.name == name).first()


def get_client_by_name(db: Session, name: str):
    return db.query(models.Client).filter(models.Client.name == name).first()


def get_service_provider_by_cpf(db: Session, cpf: str):
    return db.query(models.ServiceProvider).filter(models.ServiceProvider.cpf == cpf).first()


def get_studio_by_email(db: Session, email: str):
    return db.query(models.Studio).filter(models.Studio.email_owner == email).first()


def get_service_provider_by_email(db: Session, email: str):
    return db.query(models.ServiceProvider).filter(models.ServiceProvider.email == email).first()


def get_client_by_email(db: Session, email: str):
    return db.query(models.Client).filter(models.Client.email == email).first()


def get_client_by_cpf(db: Session, cpf: str):
    return db.query(models.Client).filter(models.Client.cpf == cpf).first()
