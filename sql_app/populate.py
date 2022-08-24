from random import choice, randint

from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal

session = SessionLocal()

name = ["Luan", "Dilermando", "Loreta", "Graca", "Lucas", "Gabriel", "Vinnie", "Carlos",
        "Giovani", "Laura", "Gilda", "Bianca", "Roberto", "Gustavo", "Ana", "Gabriel"]

last_name = ["Queiroz", "Silva", "Pereira", "Rocha", "Santos", "Pedra", "Pinto", "Gonçalves",
            "Caetano", "Wenzel", "Torchia", "Monteiro"]

email = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@npc.com", "@neko.com", "@live.com"]

description = "Lorem Ipsum is simply dummy text of the printing" +\
                "and typesetting industry. Lorem Ipsum has been the" +\
                "industry's standard dummy text ever since the 1500s," +\
                "when an unknown printer took a galley of type and" +\
                "scrambled it to make a type specimen book"

district = ["tatuape", "bela vista", "se", "moema", "paraiso", "liberdade", "cambuci", "mooca"]


"""Populate studio
"""
def populate_studio(amount: int = 10, db: Session = session):
    for i in range(amount):
        studio = {
            "name": f"studio{i}",
            "display_name": f"{choice(name)} studio",
            "country": "BRL",
            "state": "SP",
            "city": "SP",
            "district": choice(district),
            "address": "rua ficticia",
            "number": randint(1, 1000),
            "zip_code": f"{randint(100000, 999999)}",
            "complement": f"ap {randint(1, 100)}",
            "email": f"clientuser{i}{choice(email)}",
            "phone_number": f"{randint(100000000, 999999999)}",
            "description": description[:randint(1, len(description)-10)],
            "email_owner": f"studio{i}{choice(email)}"
        }

        studio = schemas.StudioCreate(**studio)
        crud.studio.create(db=db, obj_in=studio)

"""Populate service providers
"""
def populate_service(amount: int = 10, db: Session = session):
    for i in range(amount):
        service_provider = {
            "name": f"provider{i}",
            "display_name": f"{choice(name)} {choice(last_name)}",
            "cpf": f"{10000000000+i}",
            "email": f"provider{i}{choice(email)}",
            "phone_number": f"{randint(100000000, 999999999)}",
            "signal": randint(0,300),
            "description": description[:randint(1, len(description)-1)]
        }

        service_provider = schemas.ServiceProviderCreate(**service_provider)
        crud.provider.create(db=db, obj_in=service_provider)

"""Populate Client providers
"""
def populate_client(amount: int = 10, db: Session = session):
    for i in range(amount):
        client = {
            "name": f"client{i}",
            "display_name": f"{choice(name)} {choice(last_name)}",
            "birth_date": f"{randint(1960, 2004)}-{randint(1,12)}-{randint(1,27)}",
            "cpf": f"{10000000000+i}",
            "country": "BRL",
            "state": "SP",
            "city": "SP",
            "district": choice(district),
            "address": "rua corinthians",
            "number": randint(1, 1000),
            "zip_code": f"{randint(100000, 999999)}",
            "complement": f"ap {randint(1, 100)}",
            "email": f"client{i}{choice(email)}",
            "phone_number": f"{randint(100000000, 999999999)}"
        }
        
        client = schemas.ClientCreate(**client)
        crud.client.create(db=db, obj_in=client)

"""Populate sell
"""
def populate_sell(amount: int = 10, db: Session = session):
    for i in range(amount):
        sell = {
            "studio_name": f"studio{i}",
            "client_name": f"client{i}",
            "service_provider_name": f"provider{i}",
            "service_style_name": None,
            "tender_id": None,
            "price": randint(0, 1000),
            "studio_rate": randint(0, 5),
            "client_rate": randint(0, 5),
            "service_provider_rate": randint(0, 5),
            "client_suggestion_desc": description[:randint(1, 140)],
            "client_satisfied": True,
            "number_of_sessions": randint(1, 4),
            "client_contract_confirmed": True,
            "service_provider_contract_confirmed": True,
            "start_time": "2022-08-18T01:15:46.185Z",
            "last_update": "2022-08-18T01:15:46.185Z",
            "finish_time": "2022-08-18T01:15:46.185Z"
        }
        
        sell = schemas.SellCreate(**sell)
        crud.sell.create(db=db, obj_in=sell)

def main():
    populate_studio(10)
    populate_service(10)
    populate_client(10)
    populate_sell(10)

if __name__ == "__main__":
    main()
