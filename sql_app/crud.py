from sqlalchemy.orm import Session

import models, schemas

def create_service_provider(db: Session, service_provider: schemas.ServiceProvider):
    db_service_provider =  models.ServiceProvider(**service_provider.dict())

    db.add(db_service_provider)
    db.commit()
    db.refresh(db_service_provider)

    return db_service_provider

# TODO: What is to return?
def delete_service_provider_by_name(db: Session, name: str):
    db_service_provider = get_service_provider_by_name(db=db, name=name)
    
    if db_service_provider:
        db.delete(db_service_provider)
        db.commit()

        return True

    return False

def get_service_provider(db: Session):
    return db.query(models.ServiceProvider).all()

def get_service_provider_by_id(db: Session, id: int):
    return db.query(models.ServiceProvider).filter(models.ServiceProvider.id == id).first()

def get_service_provider_by_name(db: Session, name: str):
    return db.query(models.ServiceProvider).filter(models.ServiceProvider.name == name).first()

def get_service_provider_by_cpf(db: Session, cpf: str):
    return db.query(models.ServiceProvider).filter(models.ServiceProvider.cpf == cpf).first()

def get_service_provider_by_email(db: Session, email: str):
    return db.query(models.ServiceProvider).filter(models.ServiceProvider.email == email)

def create_client(db: Session, client: schemas.Client):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client

# TODO: What is to return?
def delete_client_by_name(db: Session, name: str):
    db_service_provider = get_client_by_name(db=db, name=name)
    
    if db_service_provider:
        db.delete(db_service_provider)
        db.commit()

        return True

    return False

def get_client(db: Session):
    return db.query(models.Client).all()

def get_client_by_id(db: Session, id: int):
    return db.query(models.Client).filter(models.Client.id == id).first()

def get_client_by_name(db: Session, name: str):
    return db.query(models.Client).filter(models.Client.name == name).first()

def get_client_by_cpf(db: Session, cpf: str):
    return db.query(models.Client).filter(models.Client.cpf == cpf).first()

def create_sell(db: Session, sell: schemas.Sell):
    db_sell = models.Sell(**sell.dict())
    db.add(db_sell)
    db.commit()
    db.refresh(db_sell)

    return db_sell

def create_studio(db: Session, studio:  schemas.Studio):
    ...


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


# def get_user_by_email(db: Session, email: str):
#     return db.query(models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()



