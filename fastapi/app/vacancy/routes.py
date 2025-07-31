# fastapi/app/vacancy/routes.py

# Why it's needed: exposes HTTP endpoints for creating, reading, updating, and deleting vacancies.
# Why it's named that way: routes.py is a standard file to define API routes in each module.
# What it does: connects API routes to CRUD logic using FastAPI path operations and dependency injection.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.vacancy import schemas, crud
from app.vacancy.models import Vacancy
from app.user.models import User
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

@router.post("/", response_model=schemas.VacancyRead, status_code=status.HTTP_201_CREATED)
async def create_vacancy(
    vacancy_in: schemas.VacancyCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await crud.create_vacancy(db, vacancy_in, created_by_id=current_user.id)

@router.get("/{vacancy_id}", response_model=schemas.VacancyRead)
async def read_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_async_session)):
    vacancy = await crud.get_vacancy(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return vacancy

@router.get("/", response_model=list[schemas.VacancyRead])
async def list_vacancies(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_session)):
    return await crud.get_vacancies(db, skip=skip, limit=limit)

@router.put("/{vacancy_id}", response_model=schemas.VacancyRead)
async def update_vacancy(
    vacancy_id: int,
    vacancy_in: schemas.VacancyUpdate,
    db: AsyncSession = Depends(get_async_session),
):
    vacancy = await crud.get_vacancy(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    return await crud.update_vacancy(db, vacancy, vacancy_in)

@router.delete("/{vacancy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vacancy(vacancy_id: int, db: AsyncSession = Depends(get_async_session)):
    vacancy = await crud.get_vacancy(db, vacancy_id)
    if not vacancy:
        raise HTTPException(status_code=404, detail="Vacancy not found")
    await crud.delete_vacancy(db, vacancy)
