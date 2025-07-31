# fastapi/app/company/schemas.py

# зачем нужен: описывает структуры данных для компании (вход/выход)
# почему так называется: schemas.py — стандарт для Pydantic-схем
# что делает: валидирует входные данные и сериализует выходные

from pydantic import BaseModel
from typing import Optional

class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

class CompanyPublic(CompanyBase):
    id: int

    class Config:
        orm_mode = True
