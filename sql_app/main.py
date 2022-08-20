import string
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from . import custom_logger as logging

cred = credentials.Certificate('shared/firebase-admin-private-key.json')
firebase_app = firebase_admin.initialize_app(cred)
models.Base.metadata.create_all(bind=engine)


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

def validate_token(header_autorization: string):
    try:
        bearer_token = header_autorization.split(" ")[1]
        token_verified = auth.verify_id_token(bearer_token, app=firebase_app)
        if token_verified['email_verified'] == False:
            raise HTTPException(status_code=404, detail="Email not verified")
        return True
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid Token")


@app.post("/studio/create", response_model = schemas.StudioCreate, status_code = status.HTTP_201_CREATED)
def create_studio_provider(request: Request, studio: schemas.StudioCreate, db: Session = Depends(get_db)):
    
    try:
        if validate_token(request.headers['authorization']):
            db_studio_name = crud.get_studio_by_name(db=db, name=studio.name)
            db_studio_owner_email = crud.get_studio_by_email(db=db, email=studio.email_owner)
            if db_studio_name:
                raise HTTPException(status_code=400, detail="Name already registered")
            elif db_studio_owner_email:
                raise HTTPException(status_code=400, detail="Owner email already registered")

            return crud.create_studio(db=db, studio=studio)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/provider/create", response_model = schemas.ServiceProviderCreate, status_code = status.HTTP_201_CREATED)
def create_service_provider(service_provider: schemas.ServiceProviderCreate, db: Session = Depends(get_db)):
    db_service_provider_cpf = crud.get_service_provider_by_cpf(db=db, cpf=service_provider.cpf)
    db_service_provider_name = crud.get_service_provider_by_name(db=db, name=service_provider.name)
    db_service_provider_email = crud.get_service_provider_by_email(db=db, name=service_provider.email)

    if db_service_provider_name:
        raise HTTPException(status_code=400, detail="Name already registered")
    elif db_service_provider_cpf:
        raise HTTPException(status_code=400, detail="Cpf already registered")
    elif db_service_provider_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_service_provider(db=db, service_provider=service_provider)

@app.post("/client/create", response_model = schemas.ClientCreate, status_code = status.HTTP_201_CREATED)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client_cpf = crud.get_client_by_cpf(db=db, cpf=client.cpf)
    db_client_name = crud.get_client_by_name(db=db, name=client.name)
    db_client_email = crud.get_client_by_email(db=db, email=client.email)

    if db_client_name:
        raise HTTPException(status_code=400, detail="Name already registered")
    elif db_client_cpf:
        raise HTTPException(status_code=400, detail="Cpf already registered")
    elif db_client_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    return crud.create_client(db=db, client=client)

@app.post("/sell/create", response_model=schemas.SellCreate, status_code = status.HTTP_201_CREATED)
def create_sell(sell: schemas.SellCreate, db: Session = Depends(get_db)):
    db_service_provider = crud.get_service_provider_by_name(db=db, name=sell.service_provider_name)
    db_client = crud.get_client_by_name(db=db, name=sell.client_name)

    if sell.studio_name:
        db_studio = crud.get_studio_by_name(db=db, name=sell.studio_name)

        if not db_studio:
            raise HTTPException(status_code=400, detail="This studio not exists")

    if not db_service_provider:
        raise HTTPException(status_code=400, detail="This service provider not exists")
    elif not db_client:
        raise HTTPException(status_code=400, detail="This client not exists")

    return crud.create_sell(db=db, sell=sell)

@app.get("/studio/remove")
def remove_studio_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.delete_studio_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return f"{name} deleted"

@app.get("/provider/remove")
def remove_service_provider_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.delete_service_provider_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return f"{name} deleted"

# TODO: What is to return?
@app.get("/client/remove")
def remove_client_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.delete_client_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return f"{name} deleted"

@app.get("/studios", response_model=List[schemas.Studio])
def read_studios(db: Session = Depends(get_db)):
    return crud.get_studio(db)

@app.get("/providers", response_model=List[schemas.ServiceProvider])
def read_service_providers(db: Session = Depends(get_db)):
    return crud.get_service_provider(db)

@app.get("/clients", response_model=List[schemas.Client])
def read_clients(db: Session = Depends(get_db)):
    return crud.get_client(db)

@app.get("/sells", response_model=List[schemas.Sell])
def read_sells(db: Session = Depends(get_db)):
    return crud.get_sell(db)

@app.get("/provider/", response_model = schemas.ServiceProvider)
def read_service_provider_by(name: str = None, cpf: str = None,db: Session = Depends(get_db)):
    if name:
        db_service_provider = crud.get_service_provider_by_name(db=db, name=name)
    elif cpf:
        db_service_provider = crud.get_service_provider_by_cpf(db=db, cpf=cpf)

    if db_service_provider is None:
        raise HTTPException(status_code=404, detail="Service provider not found")
    
    return db_service_provider

@app.get("/client/", response_model=schemas.Client)
def read_client_by_name(name: str = None, db: Session = Depends(get_db)):
    db_client = crud.get_client_by_name(db=db, name=name)

    if db_client is None:
        raise HTTPException(status_code=404, detail="Service provider not found")
    
    return db_client
