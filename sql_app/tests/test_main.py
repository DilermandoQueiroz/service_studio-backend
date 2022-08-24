from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_studio_create():
    response = client.post(
        "/studio/create",
        json = {
            "name": "test1",
            "display_name": "Test Api",
            "country": "BRL",
            "state": "SP",
            "city": "SP",
            "district": "Se",
            "address": "Praca da se",
            "number": 1,
            "zip_code": "0000000",
            "complement": "",
            "email": "test1@example.com",
            "phone_number": "123123123",
            "description": "test api post studio",
            "email_owner": "test1@example.com"
        },
    )
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal Server Error"}

def test_service_provider_create():
    provider = {
        "name": "test1",
        "display_name": "Test Api",
        "cpf": "123123123",
        "email": "test1@example.com",
        "phone_number": "123123123",
        "signal": 0,
        "description": "test api post studio"
        }

    response = client.post(
        "/provider/create",
        json = provider
    )
    assert response.status_code == 201
    assert response.json() == provider

def test_service_delete():
    name = "test1"
    response = client.get(f"/provider/remove/?name={name}")
    assert response.status_code == 200
    assert response.json() == f"{name} deleted"