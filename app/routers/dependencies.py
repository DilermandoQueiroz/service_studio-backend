from fastapi import HTTPException, Request
from app.db import SessionLocal
from app.firebase_utils import get_user_by_uid, validate_token
from app.custom_logger import custom_logger

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

def is_service_provider(request: Request):
    try:
        user = validate_token(request.headers['authorization'])

        if user["service_provider_id"]:
            return user
            
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=401, detail="You don't have access")

def is_owner_studio(request: Request):
    try:
        user = validate_token(request.headers['authorization'])

        user_firebase = get_user_by_uid(user['user_id'])
        is_owner = user_firebase.custom_claims.get('studio_id')

        if is_owner:
            return is_owner
        else:
            raise HTTPException(status_code=401, detail="You don't have studio")
            
    except Exception as error:
        logger.error(error)
        raise HTTPException(status_code=401, detail="You don't have studio")