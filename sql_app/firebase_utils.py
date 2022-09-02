from fastapi import HTTPException
from firebase_admin import credentials, initialize_app, auth
import schemas

cred = credentials.Certificate("shared/firebase-private-key.json")
firebase_app = initialize_app(cred)

def validate_token(header_autorization: str):
    try:
        bearer_token = header_autorization.split(" ")[1]
        token_verified = auth.verify_id_token(bearer_token, app=firebase_app)
        # if token_verified['email_verified'] == False:
        #     return False
        return token_verified
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Token")

def create_service_provider_firebase(service_provider: schemas.ServiceProviderFireBase):
    try:
        user = auth.create_user(
            email=service_provider.email,
            phone_number=service_provider.phone_number,
            password=service_provider.password,
            display_name=service_provider.display_name
        )
        if user:
            return user
        
        return False
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
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
    return auth.get_user_by_email(email)