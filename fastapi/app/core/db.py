# fastapi/app/core/db.py

# зачем нужен: этот файл создаёт async-подключение к базе данных и предоставляет асинхронную сессию для FastAPI.
# почему так называется: core — принятое название для инфраструктурных компонентов проекта; db.py — логично для кода, связанного с базой данных.
# что делает: инициализирует async SQLAlchemy (engine, sessionmaker), предоставляет базовый класс моделей и зависимость get_async_session.

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL")
# Пример: postgresql+asyncpg://user:password@host/dbname

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

async def get_async_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session
