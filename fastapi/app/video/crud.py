# fastapi/app/video/crud.py

# зачем нужен: содержит CRUD-функции для видео
# почему так называется: crud.py — стандарт для базовых операций
# что делает: создаёт записи видео в БД, будет расширяться

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert

from app.video.models import Video
from app.video.schemas import VideoCreate

async def create_video(db: AsyncSession, data: VideoCreate, user_id: int) -> Video:
    stmt = insert(Video).values(
        title=data.title,
        description=data.description,
        is_public=data.is_public,
        s3_key=data.s3_key,
        status="pending",
        created_by=user_id,
        updated_by=user_id,
    ).returning(Video)

    res = await db.execute(stmt)
    await db.commit()
    return res.scalar_one()
