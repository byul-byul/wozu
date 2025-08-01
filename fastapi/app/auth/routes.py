# fastapi/app/auth/routes.py

# зачем нужен: объявляет маршруты для регистрации, входа и подтверждения email.
# почему так называется: routes.py — общепринятое название для хранения API-эндпоинтов.
# что делает: принимает запросы, валидирует входные данные и вызывает сервис-логику.

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from app.auth import schemas, services, crud
from app.core.db import get_async_session
from sqlalchemy import select
from app.user.models import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(
    data: schemas.RegisterRequest,
    db: AsyncSession = Depends(get_async_session)
):
    await services.register_user(db, data)
    return {"message": "Check your email to verify your account."}

@router.post("/login", response_model=schemas.TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    data = schemas.LoginRequest(email=form_data.username, password=form_data.password)
    token = await services.login_user(db, data)
    return {"access_token": token}

@router.get("/verify-email")
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_async_session)
):
    email_token = await crud.get_email_token(db, token)
    if not email_token or email_token.is_used:
        return JSONResponse(status_code=400, content={"message": "Invalid or expired token"})

    if email_token.expires_at and email_token.expires_at < datetime.utcnow():
        return JSONResponse(status_code=400, content={"message": "Token expired"})

    # ⛔️ нельзя использовать email_token.user (lazy loading)
    # ✅ загружаем пользователя вручную
    result = await db.execute(select(User).where(User.id == email_token.user_id))
    user = result.scalar_one_or_none()

    if not user:
        return JSONResponse(status_code=404, content={"message": "User not found"})

    user.is_email_verified = True
    email_token.is_used = True

    await db.commit()
    return {"message": "Email verified successfully"}
