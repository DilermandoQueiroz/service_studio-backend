import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost/tattoo_python"
# SQLALCHEMY_DATABASE_URL = "postgresql://easeservice:easeservice@db:5432/tattoo_python"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
