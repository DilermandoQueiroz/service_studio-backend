from typing import List, Union

from pydantic import BaseModel


class ServiceProvider(BaseModel):
    name: str
    display_name: str
    cpf: str
    email: Union[str, None] = None 
    phone_number: Union[str, None] = None
    description: Union[str, None] = None
    

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