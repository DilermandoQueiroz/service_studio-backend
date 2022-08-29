import sys
from urllib import response
sys.path += [
    "/Users/dilermando/dev/service_studio-backend/sql_app",
    "/Users/dilermando/dev/service_studio-backend/sql_app/shared"
]

from fastapi.testclient import TestClient
from main import app
from firebase_utils import get_user_by_email

client = TestClient(app)

provider = {
    "birth_date": "2022-08-25",
    "display_name": "Test Api",
    "cpf": "123123123",
    "email": "test1@example.com",
    "phone_number": "+55123123123",
    "password": "testando1"
}

provider2 = {
    "birth_date": "2022-08-25",
    "cpf": "111111111",
    "email": "test2@example.com",
    "phone_number": "+551123123123",
    "password": "testando1"
}

def test_withou_display_name():
    response = client.post(
        "/provider/create",
        json = provider2
    )
    assert response.status_code == 422

def test_create_correct():
    response = client.post(
        "/provider/create",
        json = provider
    )
    assert response.status_code == 201

def test_create_duplicate():
    response = client.post(
        "/provider/create",
        json = provider
    )
    assert response.status_code == 500

def test_service_delete():
    user = get_user_by_email("test1@example.com")
    response = client.get(f"/provider/remove/?uid={user.uid}")
    assert response.status_code == 200