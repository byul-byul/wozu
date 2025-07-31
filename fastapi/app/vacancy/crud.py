# fastapi/app/vacancy/crud.py

# Why it's needed: implements DB logic for Vacancy operations (create, read, update, delete).
# Why it's named that way: crud.py is a standard name for database-level functions per module.
# What it does: defines async functions to manipulate Vacancy records using SQLAlchemy ORM.

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.vacancy import models, schemas

async def create_vacancy(db: AsyncSession, vacancy_in: schemas.VacancyCreate, created_by_id: int) -> models.Vacancy:
    vacancy = models.Vacancy(**vacancy_in.dict(), created_by_id=created_by_id)
    db.add(vacancy)
    await db.commit()
    await db.refresh(vacancy)
    return vacancy

async def get_vacancy(db: AsyncSession, vacancy_id: int) -> models.Vacancy | None:
    result = await db.execute(select(models.Vacancy).where(models.Vacancy.id == vacancy_id))
    return result.scalar_one_or_none()

async def get_vacancies(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Vacancy]:
    result = await db.execute(select(models.Vacancy).offset(skip).limit(limit))
    return result.scalars().all()

async def update_vacancy(db: AsyncSession, vacancy: models.Vacancy, vacancy_in: schemas.VacancyUpdate) -> models.Vacancy:
    for field, value in vacancy_in.dict(exclude_unset=True).items():
        setattr(vacancy, field, value)
    await db.commit()
    await db.refresh(vacancy)
    return vacancy

async def delete_vacancy(db: AsyncSession, vacancy: models.Vacancy) -> None:
    await db.delete(vacancy)
    await db.commit()
