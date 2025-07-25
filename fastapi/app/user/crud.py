# fastapi/app/user/crud.py

# зачем нужен: работает с БД — получает и обновляет пользователей
# почему так называется: crud.py — общепринятое имя для операций Create/Read/Update/Delete
# что делает: содержит функции для получения и обновления пользователя через SQLAlchemy

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.user.models import User
from app.user.schemas import UserUpdate

# получить пользователя по ID
async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# получить пользователя по email
async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

# обновить профиль пользователя
async def update_user(db: AsyncSession, user: User, data: UserUpdate, operator_id: int) -> User:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    user.updated_by = operator_id  # ← обязательно!
    # updated_at обновится автоматически через SQLAlchemy (если настроен onupdate)

    await db.commit()
    await db.refresh(user)
    return user
