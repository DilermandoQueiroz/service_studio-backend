from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import custom_logger as logging
import schemas
from database import Base, SessionLocal, engine
from firebase_utils import (create_service_provider_firebase, delete_by_user_uid,
                            validate_token, get_user_by_uid)

Base.metadata.create_all(bind=engine)


app = FastAPI()
origins = ["*"]
logger = logging.custom_logger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/studio/create", response_model = schemas.StudioCreate, status_code = status.HTTP_201_CREATED)
def create_studio_provider(request: Request, studio: schemas.StudioCreate, db: Session = Depends(get_db)):
    try:
        if validate_token(request.headers['authorization']):
            db_studio_name = crud.studio.get_by_name(db=db, name=studio.name)
            db_studio_owner_email = crud.studio.get_by_email(db=db, email=studio.email_owner)

            if db_studio_name:
                raise HTTPException(status_code=400, detail="Name already registered")
            elif db_studio_owner_email:
                raise HTTPException(status_code=400, detail="Owner email already registered")

            return crud.studio.create(db=db, obj_in=studio)
        else:
            raise HTTPException(status_code=401, detail="Email not verified")
    except Exception as error:
        logger.error(error)
        raise error

@app.post("/provider/create", response_model = schemas.ServiceProviderCreate, status_code = status.HTTP_201_CREATED)
def create_service_provider(service_provider: schemas.ServiceProviderAll, db: Session = Depends(get_db)):
    user = False
    try:
        user_firebase = schemas.ServiceProviderFireBase(
            display_name=service_provider.display_name,
            email=service_provider.email,
            password=service_provider.password,
            phone_number=service_provider.phone_number
        )
        user = create_service_provider_firebase(user_firebase)
        
        if user:
            db_service_provider_cpf = crud.provider.get_by_cpf(db=db, cpf=service_provider.cpf)
            db_service_provider_name = crud.provider.get_by_name(db=db, name=user.uid)
            db_service_provider_email = crud.provider.get_by_email(db=db, email=service_provider.email)
            exceptions = []

            if db_service_provider_name:
                exceptions.append("name")
            if db_service_provider_cpf:
                exceptions.append("cpf")
            if db_service_provider_email:
                exceptions.append("email")

            if exceptions:
                raise HTTPException(status_code=400, detail=f"{', '.join(exceptions)} already registered")

            user_db = schemas.ServiceProviderCreate(
                birth_date=service_provider.birth_date,
                name=user.uid,
                display_name=service_provider.display_name,
                email=service_provider.email,
                phone_number=service_provider.phone_number,
                cpf=service_provider.cpf
            )

            return crud.provider.create(db=db, obj_in=user_db)
            
    except Exception as error:
        logger.error(error)
        raise error
    finally:
        if user:
            db_service_provider_name = crud.provider.get_by_name(db=db, name=user.uid)
            if not db_service_provider_name:
                delete_by_user_uid(user.uid)


@app.post("/client/create", response_model = schemas.ClientCreate, status_code = status.HTTP_201_CREATED)
def create_client(request: Request, client: schemas.ClientCreate, db: Session = Depends(get_db)):
    try:
        user = validate_token(request.headers['authorization'])
        if user:
            db_client_cpf = crud.client.get_by_cpf(db=db, cpf=client.cpf)
            db_client_name = crud.client.get_by_name(db=db, name=client.name)
            db_client_email = crud.client.get_by_email(db=db, email=client.email)
            exceptions = []

            if db_client_name:
                exceptions.append("name")
            if db_client_cpf:
                exceptions.append("cpf")
            if db_client_email:
                exceptions.append("email")

            if len(exceptions) > 0:
                raise HTTPException(status_code=400, detail=f"{', '.join(exceptions)} already registered")

            return crud.client.create(db=db, obj_in=client)
        else:
            raise  HTTPException(status_code=400, detail="The code is not valid")
    except Exception as error:
        logger.error(error)
        print(error)

@app.post("/sell/create", response_model=schemas.SellCreate, status_code = status.HTTP_201_CREATED)
def create_sell(request: Request, sell: schemas.SellCreate, db: Session = Depends(get_db)):
    try:
        if validate_token(request.headers['authorization']):
            db_service_provider = crud.provider.get_by_email(db=db, email=sell.service_provider_name)
            db_client = crud.client.get_by_email(db=db, email=sell.client_name)
            exceptions = []

            if sell.studio_name:
                db_studio = crud.studio.get_by_name(db=db, name=sell.studio_name)

                if not db_studio:
                    exceptions.append("studio")

            if not db_service_provider:
                exceptions.append("service provider")
            if not db_client:
                exceptions.append("client")

            if len(exceptions) > 0:
                print(exceptions)
                raise HTTPException(status_code=400, detail=f"{', '.join(exceptions)} not exists")

        return crud.sell.create(db=db, obj_in=sell)
    except Exception as error:
        logger.error(error)
        raise error
        
@app.get("/studio/remove")
def remove_studio_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.studio.remove_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return response

@app.get("/provider/remove")
def remove_service_provider_by_name(uid: str = None, db: Session = Depends(get_db)):
    try:
        response = crud.provider.remove_by_name(db=db, name=uid)
        
        if not response:
            raise HTTPException(status_code=400, detail="Uid not exists")
        
        delete_by_user_uid(uid)

        return response
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/client/remove")
def remove_client_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.client.remove_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return response

@app.get("/studios", response_model=List[schemas.StudioInDBBase])
def read_studios(db: Session = Depends(get_db)):
    return crud.studio.get_all(db)

@app.get("/providers", response_model=List[schemas.ServiceProviderInDBBase])
def read_service_providers(db: Session = Depends(get_db)):
    return crud.provider.get_all(db)

@app.get("/clients", response_model=List[schemas.ClientInDBBase])
def read_clients(db: Session = Depends(get_db)):
    return crud.client.get_all(db)

@app.get("/sells", response_model=List[schemas.SellInDBBase])
def read_sells(db: Session = Depends(get_db)):
    return crud.sell.get_all(db)


# @app.get("/provider/", response_model = schemas.ServiceProviderInDBBase)
# def read_service_provider_by(name: str = None, cpf: str = None, email: str = None, db: Session = Depends(get_db)):
#     db_service_provider = False

#     if name:
#         db_service_provider = crud.provider.get_by_name(db=db, name=name)
#     elif email:
#         db_service_provider = crud.provider.get_by_email(db=db, email=email)
#     elif cpf:
#         db_service_provider = crud.provider.get_by_cpf(db=db, cpf=cpf)

#     if not db_service_provider:
#         raise HTTPException(status_code=404, detail="Service provider not found")
    
#     return db_service_provider

# @app.get("/client/", response_model=schemas.ClientInDBBase)
# def read_client_by_name(name: str = None, email: str = None, db: Session = Depends(get_db)):
#     if name:
#         db_client = crud.client.get_by_name(db=db, name=name)
#     elif email:
#         db_client = crud.client.get_by_email(db=db, email=email)
#     if db_client is None:
#         raise HTTPException(status_code=404, detail="Service provider not found")
    
#     return db_client

@app.get("/sell_by_email/", response_model=List[schemas.SellInDBBase])
def sell_by_email(request: Request, db: Session = Depends(get_db)):
    user = validate_token(request.headers['authorization'])
    if user:
        db_client = crud.sell.get_by_provider_email(db=db, service_provider_email=user['email'])
        if db_client is None:
            raise HTTPException(status_code=404, detail="Clients not found")
        return db_client

@app.get("/get_providers_clients", response_model=List[schemas.ClientInDBBase])
def get_providers_clients(request: Request, db: Session = Depends(get_db)):
    user = validate_token(request.headers['authorization'])
    if user:
        db_client = crud.sell.get_unique_by_provider_email(db=db, service_provider_email=user['email'])

        return db_client