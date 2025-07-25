# fastapi/app/user/schemas.py

# зачем нужен: описывает структуры данных для пользователей (вход/выход)
# почему так называется: schemas.py — стандарт для Pydantic-схем
# что делает: валидация и сериализация данных пользователей

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# базовая схема — общие поля профиля, которые используются в других схемах
class UserBase(BaseModel):
    email: EmailStr
    phone: str
    full_name: Optional[str]
    nick_name: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    birth_date: Optional[date]
    gender: Optional[str]
    photo_url: Optional[str]

# ответ клиенту (например, в /user/me)
# включает базовые поля + флаги верификации и последний вход
class UserPublic(UserBase):
    is_email_verified: bool
    is_phone_verified: bool
    last_login_at: Optional[datetime]

    class Config:
        orm_mode = True  # позволяет работать с ORM-моделью напрямую

# схема обновления профиля (в PUT-запросах)
# включает только редактируемые поля, без email/phone
class UserUpdate(BaseModel):
    full_name: Optional[str]
    nick_name: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    birth_date: Optional[date]
    gender: Optional[str]
    photo_url: Optional[str]
