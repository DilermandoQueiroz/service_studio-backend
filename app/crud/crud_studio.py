from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from app.models import Studio
from app.schemas import StudioCreate, StudioUpdate


class CRUDStudio(CRUDBase[Studio, StudioCreate, StudioUpdate]):
    ...


studio = CRUDStudio(Studio)