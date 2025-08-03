# fastapi/app/video/schemas.py

# Why it's needed: defines input/output validation for video endpoints.
# Why it's named that way: common convention for Pydantic schemas.
# What it does: defines data formats for reading/creating/updating videos.

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class VideoStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    rejected = "rejected"

class VideoBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_public: bool = True

class VideoCreate(VideoBase):
    s3_key: str

class VideoUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    is_public: Optional[bool]

class VideoRead(VideoBase):
    id: int
    user_id: int
    s3_key: str
    thumbnail_url: Optional[str]
    mime_type: Optional[str]
    file_size: Optional[int]  # bytes
    duration: Optional[float]  # seconds
    status: str  # or VideoStatus if model switched
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
