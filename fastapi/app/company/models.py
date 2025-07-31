# fastapi/app/company/models.py

# зачем нужен: описывает таблицу компаний, к которым могут принадлежать пользователи
# почему так называется: models.py — общепринятое имя для моделей БД
# что делает: определяет структуру таблицы companies

from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.models import BaseDBModel

class Company(BaseDBModel):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String, nullable=True)
    website: Mapped[str | None] = mapped_column(String, nullable=True)
    location: Mapped[str | None] = mapped_column(String, nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="company")