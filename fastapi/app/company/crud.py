# fastapi/app/company/crud.py

# зачем нужен: содержит функции доступа к данным компаний
# почему так называется: crud.py — общепринятое название для логики Create/Read/Update/Delete
# что делает: реализует логику создания, получения и обновления компаний

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.company import models, schemas
from app.core.models import BaseDBModel

async def create_company(
    db: AsyncSession,
    data: schemas.CompanyCreate,
    owner_id: int
) -> models.Company:
    company = models.Company(**data.dict(), created_by=owner_id, updated_by=owner_id)
    db.add(company)
    await db.commit()
    await db.refresh(company)
    return company

async def get_company_by_id(db: AsyncSession, company_id: int) -> models.Company | None:
    result = await db.execute(
        select(models.Company).where(models.Company.id == company_id)
    )
    return result.scalar_one_or_none()

async def update_company(
    db: AsyncSession,
    company: models.Company,
    data: schemas.CompanyUpdate,
    operator_id: int
) -> models.Company:
    for field, value in data.dict(exclude_unset=True).items():
        setattr(company, field, value)
    company.updated_by = operator_id
    await db.commit()
    await db.refresh(company)
    return company
