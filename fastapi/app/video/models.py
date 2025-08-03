# fastapi/app/video/models.py

# Зачем нужен: описывает таблицу Video
# Почему так называется: логическая модель видео
# Что делает: хранит метаинформацию, статус, привязку к юзеру

from sqlalchemy import String, Integer, ForeignKey, Boolean, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4
from app.core.models import BaseDBModel

class Video(BaseDBModel):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    s3_key: Mapped[str] = mapped_column(String, unique=True)
    thumbnail_url: Mapped[str | None] = mapped_column(String, nullable=True)
    is_public: Mapped[bool] = mapped_column(default=True)
    status: Mapped[str] = mapped_column(String(32), default="pending")
    duration: Mapped[int | None] = mapped_column(nullable=True)  # seconds
    file_size: Mapped[int | None] = mapped_column(nullable=True)  # bytes
    mime_type: Mapped[str | None] = mapped_column(String, nullable=True)