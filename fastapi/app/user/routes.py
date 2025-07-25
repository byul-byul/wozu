# fastapi/app/user/routes.py

# зачем нужен: предоставляет маршруты для получения и обновления профиля
# почему так называется: routes.py — стандартное место для описания эндпоинтов
# что делает: описывает API /user/me и /user/stats

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.user import crud
from app.user.schemas import UserPublic, UserUpdate
from app.user.models import User
from app.core.db import get_async_session
from app.auth.dependencies import get_current_user  # ← обновлено под HTTPBearer

router = APIRouter(prefix="/user", tags=["user"])

# получить текущий профиль
@router.get("/me", response_model=UserPublic)
async def get_me(
    current_user: User = Depends(get_current_user)
) -> UserPublic:
    return current_user

# обновить текущий профиль
@router.put("/me", response_model=UserPublic)
async def update_me(
    data: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user)
) -> UserPublic:
    updated = await crud.update_user(db, current_user, data, operator_id=current_user.id)
    return updated
