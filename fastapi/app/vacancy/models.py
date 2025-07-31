# fastapi/app/vacancy/models.py

# Why it's needed: defines the Vacancy model representing job listings in the system.
# Why it's named that way: models.py holds SQLAlchemy models related to the vacancy module.
# What it does: declares the database structure for job vacancies, linked to a company and creator.

from sqlalchemy import String, Text, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models import BaseDBModel

class Vacancy(BaseDBModel):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    address: Mapped[str | None] = mapped_column(String, nullable=True)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"), nullable=False)
    company: Mapped["Company"] = relationship()

    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_by: Mapped["User"] = relationship()
