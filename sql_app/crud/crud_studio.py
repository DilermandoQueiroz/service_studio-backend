from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from models import Studio
from schemas import StudioCreate, StudioInDBBase


class CRUDItem(CRUDBase[Studio, StudioCreate, StudioInDBBase]):
    ...


studio = CRUDItem(Studio)