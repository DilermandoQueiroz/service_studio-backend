from fastapi import HTTPException, Request
from db import SessionLocal
from firebase_utils import validate_token
from custom_logger import custom_logger

logger = custom_logger(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def validate_token_client(request: Request):
    try:
        user = validate_token(request.headers['authorization'])
        if user:
            return user
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=401, detail="You don't have access")
