from fastapi.testclient import TestClient
from fastapi import FastAPI


app = FastAPI()
client = TestClient(app)

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