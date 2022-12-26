from fastapi.testclient import TestClient
from fastapi import FastAPI


app = FastAPI()
client = TestClient(app)

# def test_studio_create():
#     response = client.post(
#         "/studio/create",
#         json = {
#             "name": "test1",
#             "display_name": "Test Api",
#             "country": "BRL",
#             "state": "SP",
#             "city": "SP",
#             "district": "Se",
#             "address": "Praca da se",
#             "number": 1,
#             "zip_code": "0000000",
#             "complement": "",
#             "email": "test1@example.com",
#             "phone_number": "123123123",
#             "description": "test api post studio",
#             "email_owner": "test1@example.com"
#         },
#     )
#     assert response.status_code == 500
#     assert response.json() == {"detail": "Internal Server Error"}