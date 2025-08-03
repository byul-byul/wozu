# fastapi/app/video/routes.py

# Why it's needed: defines endpoints to upload and manage videos.
# Why it's named that way: routes.py stores HTTP route definitions.
# What it does: defines endpoints for CRUD operations on videos.

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.video import schemas, crud
from app.core.db import get_async_session
from app.auth.dependencies import get_current_user
from app.user.models import User

router = APIRouter(prefix="/videos", tags=["videos"])

@router.post("/", response_model=schemas.VideoRead, status_code=status.HTTP_201_CREATED)
async def create_video(
    data: schemas.VideoCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
):
    return await crud.create_video(db, data, current_user.id)

@router.get("/", response_model=list[schemas.VideoRead])
async def list_videos(
    db: AsyncSession = Depends(get_async_session),
    skip: int = 0,
    limit: int = 100,
):
    return await crud.get_videos(db, skip=skip, limit=limit)

@router.get("/{video_id}", response_model=schemas.VideoRead)
async def get_video(video_id: int, db: AsyncSession = Depends(get_async_session)):
    video = await crud.get_video(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
