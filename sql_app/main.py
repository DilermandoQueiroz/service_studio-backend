from typing import List

from fastapi import Depends, FastAPI, HTTPException
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

@app.post("/provider/create", response_model = schemas.ServiceProvider)
def create_service_provider(service_provider: schemas.ServiceProvider, db: Session = Depends(get_db)):
    db_service_provider_cpf = crud.get_service_provider_by_cpf(db=db, cpf=service_provider.cpf)
    db_service_provider_name = crud.get_service_provider_by_name(db=db, name=service_provider.name)
    
    if db_service_provider_name:
        raise HTTPException(status_code=400, detail="Name already registered")
    elif db_service_provider_cpf:
        raise HTTPException(status_code=400, detail="Cpf already registered")

    return crud.create_service_provider(db=db, service_provider=service_provider)

# TODO: What is to return?
@app.get("/provider/delete")
def remove_service_provider_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.delete_service_provider_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return f"{name} deleted"

@app.get("/providers", response_model = List[schemas.ServiceProvider])
def read_service_provider(db: Session = Depends(get_db)):
    return crud.get_service_provider(db)

@app.get("/provider/", response_model = schemas.ServiceProvider)
def read_service_provider_by(name: str = None, cpf: str = None,db: Session = Depends(get_db)):
    if name:
        db_service_provider = crud.get_service_provider_by_name(db=db, name=name)
    elif cpf:
        db_service_provider = crud.get_service_provider_by_cpf(db=db, cpf=cpf)

    if db_service_provider is None:
        raise HTTPException(status_code=404, detail="Service provider not found")
    
    return db_service_provider

@app.post("/client/create")
def create_client(client: schemas.Client, db: Session = Depends(get_db)):
    db_client_cpf = crud.get_client_by_cpf(db=db, cpf=client.cpf)
    db_client_name = crud.get_client_by_name(db=db, name=client.name)

    if db_client_name:
        raise HTTPException(status_code=400, detail="Name already registered")
    elif db_client_cpf:
        raise HTTPException(status_code=400, detail="Cpf already registered")

    return crud.create_client(db=db, client=client)

# TODO: What is to return?
@app.get("/client/remove")
def remove_client_by_name(name: str = None, db: Session = Depends(get_db)):
    response = crud.delete_client_by_name(db=db, name=name)

    if not response:
        raise HTTPException(status_code=400, detail="Name not exists")
    
    return f"{name} deleted"

@app.get("/clients")
def read_client(db: Session = Depends(get_db)):
    return crud.get_client(db)