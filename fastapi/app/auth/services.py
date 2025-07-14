# fastapi/app/auth/services.py

# зачем нужен: содержит бизнес-логику модуля auth (регистрация, логин, подтверждение email).
# почему так называется: services.py — стандартное имя для слоя между API и БД, где живёт логика приложения.
# что делает: управляет процессами регистрации, входа, создания токенов и вызова email-отправки.

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.auth import crud, security, email_utils
from app.users.models import User
from app.auth.schemas import RegisterRequest, LoginRequest

async def register_user(db: AsyncSession, data: RegisterRequest) -> None:
    existing_user = await crud.get_user_by_email(db, data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = security.hash_password(data.password)
    user = User(email=data.email, hashed_password=hashed_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token_obj = await crud.create_email_token(db, user.id)
    email_utils.send_verification_email(user.email, token_obj.token)

async def login_user(db: AsyncSession, data: LoginRequest) -> str:
    user = await crud.get_user_by_email(db, data.email)
    if not user or not security.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return security.create_access_token(user.id)
