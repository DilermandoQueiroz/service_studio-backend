from fastapi import HTTPException
from firebase_admin import credentials, initialize_app, auth
from pydantic import UUID4
import app.schemas as schemas

cred = credentials.Certificate("app/shared/firebase-private-key.json")
firebase_app = initialize_app(cred)

def validate_token(header_autorization: str):
    try:
        bearer_token = header_autorization.split(" ")[1]
        token_verified = auth.verify_id_token(bearer_token, app=firebase_app)

        return token_verified
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")

def create_service_provider_firebase(
    service_provider: schemas.ServiceProviderCreateFirebase,
    service_provider_id: UUID4 = None,
    person_id: UUID4 = None
    ):
    try:
        user = auth.create_user(
            email=service_provider.email,
            password=service_provider.password,
            display_name=service_provider.display_name
        )
        if user:
            auth.set_custom_user_claims(user.uid, {
                "service_provider_id": str(service_provider_id),
                "person_id": str(person_id),
                "studio_id": False
            })

            return user
        
        return False
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def create_studio(uid: str, studio_id: UUID4):
    user = get_user_by_uid(uid=uid)

    auth.set_custom_user_claims(user.uid, {
            "service_provider_id": user.custom_claims.get('service_provider_id'),
            "person_id": user.custom_claims.get('person_id'),
            "studio_id": str(studio_id)
    })

def delete_by_user_uid(uid: str):
    try:
        auth.delete_user(uid)
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def delete_by_email(email: str):
    try:
        user = get_user_by_email(email)

        delete_by_user_uid(user.uid)
    except Exception as error:
        raise error

def get_user_by_uid(uid: str):
    try:
        user = auth.get_user(uid)
        if user:
            return user
        
        return False
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

def get_user_by_email(email: str):
    try:
        return auth.get_user_by_email(email)
    except:
        return False