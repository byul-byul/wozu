# fastapi/app/company/routes.py

# зачем нужен: предоставляет API для управления компаниями
# почему так называется: routes.py — стандартное имя для маршрутов FastAPI
# что делает: описывает эндпоинты создания, получения и обновления компаний

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.auth.dependencies import get_current_user
from app.user.models import User
from app.company import schemas, crud

router = APIRouter(prefix="/companies", tags=["companies"])

@router.post("/", response_model=schemas.CompanyPublic)
async def create_company(
    data: schemas.CompanyCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await crud.create_company(db, data, owner_id=current_user.id)

@router.get("/{company_id}", response_model=schemas.CompanyPublic)
async def get_company(
    company_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    company = await crud.get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=schemas.CompanyPublic)
async def update_company(
    company_id: int,
    data: schemas.CompanyUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    company = await crud.get_company_by_id(db, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return await crud.update_company(db, company, data, operator_id=current_user.id)
