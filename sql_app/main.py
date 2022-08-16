from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

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
def create_studio_provider(studio: schemas.StudioCreate, db: Session = Depends(get_db)):
    db_studio_name = crud.get_studio_by_name(db=db, name=studio.name)
    
    if db_studio_name:
        raise HTTPException(status_code=400, detail="Name already registered")
    
    return crud.create_studio(db=db, studio=studio)

@app.post("/provider/create", response_model = schemas.ServiceProviderCreate, status_code = status.HTTP_201_CREATED)
def create_service_provider(service_provider: schemas.ServiceProviderCreate, db: Session = Depends(get_db)):
    db_service_provider_cpf = crud.get_service_provider_by_cpf(db=db, cpf=service_provider.cpf)
    db_service_provider_name = crud.get_service_provider_by_name(db=db, name=service_provider.name)
    
    if db_service_provider_name:
        raise HTTPException(status_code=400, detail="Name already registered")
    elif db_service_provider_cpf:
        raise HTTPException(status_code=400, detail="Cpf already registered")

    return crud.create_service_provider(db=db, service_provider=service_provider)

@app.post("/client/create", response_model = schemas.ClientCreate, status_code = status.HTTP_201_CREATED)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client_cpf = crud.get_client_by_cpf(db=db, cpf=client.cpf)
    db_client_name = crud.get_client_by_name(db=db, name=client.name)

    if db_client_name:
        raise HTTPException(status_code=400, detail="Name already registered")
    elif db_client_cpf:
        raise HTTPException(status_code=400, detail="Cpf already registered")

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

@app.get("/clients")
def read_clients(db: Session = Depends(get_db)):
    return crud.get_client(db)

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
