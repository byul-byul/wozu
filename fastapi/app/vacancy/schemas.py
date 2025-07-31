# fastapi/app/vacancy/schemas.py

# Why it's needed: defines data validation and serialization schemas for Vacancy.
# Why it's named that way: schemas.py is a convention for holding Pydantic models in each module.
# What it does: declares base, create, update, and read schemas for Vacancy used in API and DB I/O.

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VacancyBase(BaseModel):
    title: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    address: Optional[str] = None
    company_id: int

class VacancyCreate(VacancyBase):
    pass

class VacancyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    company_id: Optional[int] = None

class VacancyRead(VacancyBase):
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
