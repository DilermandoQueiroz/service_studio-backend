from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from models import Sell
from schemas import SellCreate, SellInDBBase


class CRUDSell(CRUDBase[Sell, SellCreate, SellInDBBase]):
    ...


sell = CRUDSell(Sell)