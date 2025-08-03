# fastapi/app/video/models.py

# Why it's needed: stores video metadata (not actual video file).
# Why it's named that way: this file defines DB model for videos.
# What it does: defines the Video SQLAlchemy model linked to a user.

from sqlalchemy import String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.core.models import BaseDBModel  # ✅ включает id, created_at, etc.

class Video(BaseDBModel):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    s3_key: Mapped[str] = mapped_column(String(255))  # example: 'videos/abc123.mp4'
    thumbnail_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    mime_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    file_size: Mapped[int | None] = mapped_column(nullable=True)  # bytes
    duration: Mapped[float | None] = mapped_column(nullable=True)  # seconds

    status: Mapped[str] = mapped_column(String(32), default="ready")
    is_public: Mapped[bool] = mapped_column(default=True)
