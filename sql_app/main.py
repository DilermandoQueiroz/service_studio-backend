from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import custom_logger as logging
from database import Base, engine
from routers import (client_route, sell_route, service_provider_route,
                     studio_route)

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(studio_route.router)
app.include_router(service_provider_route.router)
app.include_router(client_route.router)
app.include_router(sell_route.router)
origins = ["*"]
logger = logging.custom_logger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
