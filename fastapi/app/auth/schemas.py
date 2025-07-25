# fastapi/app/auth/schemas.py

# зачем нужен: этот файл содержит Pydantic-схемы, описывающие структуру входных и выходных данных для эндпоинтов.
# почему так называется: schemas.py — принятое имя для хранения Pydantic-моделей (аналог моделей данных, но без привязки к БД).
# что делает: описывает структуру данных, которую ожидает и возвращает API. Используется в роутинге и валидации запросов.

from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    email: EmailStr
    phone: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
