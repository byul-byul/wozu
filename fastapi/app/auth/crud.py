# fastapi/app/auth/crud.py

# зачем нужен: реализует логику работы с базой данных для модуля auth.
# почему так называется: crud — общепринятое имя для Create/Read/Update/Delete операций в БД.
# что делает: создаёт токены подтверждения, ищет пользователей по email, помечает токены как использованные и т.д.

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.auth.models import EmailToken
from app.users.models import User
from datetime import datetime
import uuid
from sqlalchemy.orm import joinedload

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_email_token(db: AsyncSession, user_id: int) -> EmailToken:
    token = str(uuid.uuid4())
    email_token = EmailToken(user_id=user_id, token=token)
    db.add(email_token)
    await db.commit()
    await db.refresh(email_token)
    return email_token

async def get_email_token(db: AsyncSession, token: str) -> EmailToken | None:
    result = await db.execute(
        select(EmailToken)
        .where(EmailToken.token == token, EmailToken.is_used == False)
        .options(joinedload(EmailToken.user))  # ← подтягиваем user заранее
    )
    return result.scalar_one_or_none()

async def mark_token_used(db: AsyncSession, token: str):
    await db.execute(
        update(EmailToken).where(EmailToken.token == token).values(is_used=True)
    )
    await db.commit()
