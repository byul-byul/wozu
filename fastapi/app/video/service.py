# fastapi/app/video/service.py

# зачем нужен: бизнес-логика генерации presigned URL и фоновой обработки видео
# почему так называется: service — принятое имя для логики вне crud
# что делает: генерирует уникальный s3_key, presigned PUT URL и обрабатывает видео после загрузки

import uuid
import os
import json
import tempfile
import subprocess
from datetime import datetime

from boto3 import client
from botocore.client import Config
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select

from app.video.models import Video
from app.video.schemas import PresignResponse, VideoStatus

S3_BUCKET = os.getenv("S3_BUCKET_NAME", "wozu")
S3_EXPIRE = 600

s3 = client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL"),
    aws_access_key_id=os.getenv("S3_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("S3_SECRET_KEY"),
    config=Config(signature_version="s3v4"),
    region_name="auto",
)

def generate_presign_url() -> PresignResponse:
    video_id = str(uuid.uuid4())
    s3_key = f"videos/{video_id}.mp4"

    url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": S3_BUCKET, "Key": s3_key},
        ExpiresIn=S3_EXPIRE,
        HttpMethod="PUT"
    )

    return PresignResponse(
        upload_url=url,
        s3_key=s3_key,
        expires_in=S3_EXPIRE
    )

async def process_video(video_id: int, session: AsyncSession):
    result = await session.execute(select(Video).where(Video.id == video_id))
    video = result.scalar_one_or_none()
    if not video:
        return

    await session.execute(update(Video).where(Video.id == video_id).values(status=VideoStatus.processing))
    await session.commit()

    video_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": S3_BUCKET, "Key": video.s3_key},
        ExpiresIn=600
    )

    try:
        probe_result = subprocess.run(
            ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", video_url],
            capture_output=True, text=True, check=True
        )
        probe_data = json.loads(probe_result.stdout)
        duration = float(probe_data["format"]["duration"])
        file_size = int(probe_data["format"]["size"])
        mime_type = probe_data["format"]["format_name"]
    except Exception:
        await session.execute(update(Video).where(Video.id == video_id).values(status=VideoStatus.rejected))
        await session.commit()
        return

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_thumb:
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-i", video_url, "-ss", "00:00:01", "-vframes", "1", "-q:v", "2", tmp_thumb.name],
                check=True
            )
            thumb_key = f"thumbnails/{video_id}.jpg"
            s3.upload_file(tmp_thumb.name, S3_BUCKET, thumb_key)
            thumbnail_url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": S3_BUCKET, "Key": thumb_key},
                ExpiresIn=3600
            )
        finally:
            os.unlink(tmp_thumb.name)

    await session.execute(update(Video).where(Video.id == video_id).values(
        status=VideoStatus.moderation,
        duration=int(duration),
        file_size=file_size,
        mime_type=mime_type,
        thumbnail_url=thumbnail_url,
        updated_at=datetime.utcnow(),
    ))
    await session.commit()
