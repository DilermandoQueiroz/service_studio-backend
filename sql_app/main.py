import string
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session
import crud, schemas
from database import SessionLocal, engine, Base
import custom_logger as logging

cred = credentials.Certificate('shared/firebase-private-key.json')
firebase_app = firebase_admin.initialize_app(cred)
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

def validate_token(header_autorization: string):
    try:
        bearer_token = header_autorization.split(" ")[1]
        token_verified = auth.verify_id_token(bearer_token, app=firebase_app)
        if token_verified['email_verified'] == False:
            return False
        return True
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")

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
def create_service_provider(service_provider: schemas.ServiceProviderCreate, db: Session = Depends(get_db)):
    try:
        db_service_provider_cpf = crud.provider.get_by_cpf(db=db, cpf=service_provider.cpf)
        db_service_provider_name = crud.provider.get_by_name(db=db, name=service_provider.name)
        db_service_provider_email = crud.provider.get_by_email(db=db, email=service_provider.email)
        exceptions = []

        if db_service_provider_name:
            exceptions.append("name")
        if db_service_provider_cpf:
            exceptions.append("cpf")
        if db_service_provider_email:
            exceptions.append("email")

        if len(exceptions) > 0:
            raise HTTPException(status_code=400, detail=f"{', '.join(exceptions)} already registered")

        return crud.provider.create(db=db, obj_in=service_provider)
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/client/create", response_model = schemas.ClientCreate, status_code = status.HTTP_201_CREATED)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    # TODO: validate uid - token 
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

@app.post("/sell/create", response_model=schemas.SellCreate, status_code = status.HTTP_201_CREATED)
def create_sell(sell: schemas.SellCreate, db: Session = Depends(get_db)):
    db_service_provider = crud.provider.get_by_name(db=db, name=sell.service_provider_name)
    db_client = crud.client.get_by_name(db=db, name=sell.client_name)
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
        raise HTTPException(status_code=400, detail=f"{', '.join(exceptions)} not exists")

    return crud.sell.create(db=db, obj_in=sell)

@app.get("/studio/remove")
def remove_studio_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.studio.remove_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return response

@app.get("/provider/remove")
def remove_service_provider_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.provider.remove_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return response

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

@app.get("/provider/", response_model = schemas.ServiceProviderInDBBase)
def read_service_provider_by(name: str = None, cpf: str = None, email: str = None, db: Session = Depends(get_db)):
    db_service_provider = False

    if name:
        db_service_provider = crud.provider.get_by_name(db=db, name=name)
    elif email:
        db_service_provider = crud.provider.get_by_email(db=db, email=email)
    elif cpf:
        db_service_provider = crud.provider.get_by_cpf(db=db, cpf=cpf)

    if not db_service_provider:
        raise HTTPException(status_code=404, detail="Service provider not found")
    
    return db_service_provider

@app.get("/client/", response_model=schemas.ClientInDBBase)
def read_client_by_name(name: str = None, email: str = None, db: Session = Depends(get_db)):
    if name:
        db_client = crud.client.get_by_name(db=db, name=name)
    elif email:
        db_client = crud.client.get_by_email(db=db, email=email)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Service provider not found")
    
    return db_client
