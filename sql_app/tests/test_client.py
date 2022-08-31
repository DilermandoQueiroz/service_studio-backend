import sys

sys.path += [
    "/Users/dilermando/dev/service_studio-backend/sql_app",
    "/Users/dilermando/dev/service_studio-backend/sql_app/shared"
]

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

client = {
    "name": "Test 1",
    "display_name": "Test API",
    "birth_date": "",
    "cpf": "33602461017",
    "country": "BRL",
    "state": "SP",
    "city": "SP",
    "district": "Test",
    "address": "rua corinthians",
    "number": 10,
    "zip_code": "1230123",
    "complement": "b",
    "email": "client_test@example.com",
    "phone_number": "+551198576"
}