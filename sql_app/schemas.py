from typing import Union

from pydantic import BaseModel


class ServiceProvider(BaseModel):
    name: str
    display_name: str
    cpf: str
    email: Union[str, None] = None
    phone_number: Union[str, None] = None
    signal: Union[int, None] = None
    description: Union[str, None] = None

    class Config:
        orm_mode = True
    

class Client(BaseModel):
    name: str
    display_name: str
    birth_date: str
    cpf: str
    country: Union[str, None] = None 
    state: Union[str, None] = None 
    city: Union[str, None] = None
    district: Union[str, None] = None
    address: Union[str, None] = None
    number: Union[int, None] = None
    zip_code: Union[str, None] = None
    complement: Union[str, None] = None 
    email: Union[str, None] = None 
    phone_number: Union[str, None] = None

    class Config:
        orm_mode = True

class Sell(BaseModel):
    service_provider: str
    studio: Union[str, None] = None
    client: str
    service_style: Union[int, None] = None
    tender: Union[int, None] = None
    price: int
    studio_rate: Union[int, None] = None
    client_rate: Union[int, None] = None
    service_provider_rate: Union[int, None] = None
    client_suggestion_desc: Union[str, None] = None
    client_satisfied: Union[bool, None] = None
    number_of_sessions: int
    client_contract_confirmed: Union[bool, None] = None
    service_provider_contract_confirmed: Union[bool, None] = None
    start_time: str
    last_update: Union[str, None] = None
    finish_time: Union[str, None] = None 
    phone_number: Union[str, None] = None

    class Config:
        orm_mode = True

class Studio(BaseModel):
    name: str
    display_name: str
    birth_date: str
    cpf: str
    country: Union[str, None] = None 
    state: Union[str, None] = None 
    city: Union[str, None] = None
    district: Union[str, None] = None
    address: Union[str, None] = None
    number: Union[int, None] = None
    zip_code: Union[str, None] = None
    complement: Union[str, None] = None
    email: Union[str, None] = None 
    phone_number: Union[str, None] = None
    description: Union[str, None] = None
    email_owner = str

    class Config:
        orm_mode = True

    # TODO: confirm with luan
    # sell = relationship("Sell", back_populates="studio", uselist=False)
    # service_providers = relationship("ServiceProvider", secondary=association_table_service_provider_studio, back_populates="studios")