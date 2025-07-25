# fastapi/app/core/models.py

# зачем нужен: содержит базовую модель BaseDBModel со служебными полями, наследуемую всеми таблицами.
# почему так называется: models.py — стандартное имя для моделей; core/ — потому что используется везде.
# что делает: определяет абстрактную базу для SQLAlchemy-моделей с created_at, updated_by и пр.

from sqlalchemy import Column, Integer, Boolean, DateTime, func
from app.core.db import Base

class BaseDBModel(Base):
    __abstract__ = True

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
