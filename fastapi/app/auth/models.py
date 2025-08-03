# fastapi/app/auth/models.py

# зачем нужен: этот файл содержит ORM-модели SQLAlchemy, то есть определения таблиц базы данных через Python-классы.
# почему так называется: это устоявшееся имя в Python-проектах (Django, FastAPI, Flask): models.py = "бизнес-сущности + таблицы БД"
# что делает: в models.py ты описываешь таблицы, которые потом будут: автоматически созданы Alembic-миграцией, использоваться в CRUD, сервисах, роутинге.

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.models import BaseDBModel

class EmailToken(BaseDBModel):
    __tablename__ = "email_tokens"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    token = Column(String, unique=True, nullable=False, index=True)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime)  # новое поле

    user = relationship("User", back_populates="email_tokens")
