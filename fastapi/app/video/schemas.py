# fastapi/app/video/schemas.py

# зачем нужен: описывает Pydantic-схемы для валидации и сериализации видео
# почему так называется: schemas.py — общепринятый файл для Pydantic моделей
# что делает: определяет входные/выходные данные для API

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class VideoStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    moderation = "moderation"
    approved = "approved"
    rejected = "rejected"
    archived = "archived"

class VideoCreate(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    is_public: bool = True
    s3_key: str

class VideoRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_public: bool
    s3_key: str
    thumbnail_url: Optional[str]
    status: VideoStatus

    class Config:
        orm_mode = True

class PresignResponse(BaseModel):
    upload_url: str
    s3_key: str
    expires_in: int
