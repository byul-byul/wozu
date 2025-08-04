# fastapi/app/video/routes.py

# зачем нужен: содержит API-эндпоинты для работы с видео
# почему так называется: routes.py — стандартное имя для API-маршрутов
# что делает: принимает входные данные и вызывает CRUD/сервисы

from fastapi import APIRouter, Depends, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_async_session
from app.auth.dependencies import get_current_user
from app.video.schemas import VideoCreate, VideoRead, PresignResponse
from app.video.crud import create_video
from app.video.service import generate_presign_url, process_video
from app.user.models import User

router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/", response_model=VideoRead, status_code=status.HTTP_201_CREATED)
async def upload_video(
    data: VideoCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user),
):
    video = await create_video(session, data, user.id)
    background_tasks.add_task(process_video, video.id, session)
    return video

@router.get("/presign-upload/", response_model=PresignResponse)
async def get_presigned_upload_url(
    user: User = Depends(get_current_user),
):
    return generate_presign_url()
