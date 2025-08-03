# fastapi/app/video/crud.py

# Why it's needed: defines DB logic for video operations (create, list, retrieve).
# Why it's named that way: CRUD — standard acronym for Create, Read, Update, Delete.
# What it does: implements async DB queries using SQLAlchemy.

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.video import models, schemas

async def create_video(db: AsyncSession, data: schemas.VideoCreate, user_id: int) -> models.Video:
    new_video = models.Video(
        user_id=user_id,
        title=data.title,
        description=data.description,
        s3_key=data.s3_key,
        thumbnail_url=data.thumbnail_url,
        mime_type=data.mime_type,
        file_size=data.file_size,
        duration=data.duration,
        status=data.status,
        is_public=data.is_public,
    )
    db.add(new_video)
    await db.commit()
    await db.refresh(new_video)
    return new_video

async def get_videos(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[models.Video]:
    result = await db.execute(select(models.Video).offset(skip).limit(limit))
    return result.scalars().all()

async def get_video(db: AsyncSession, video_id: int) -> models.Video | None:
    result = await db.execute(select(models.Video).where(models.Video.id == video_id))
    return result.scalar_one_or_none()
