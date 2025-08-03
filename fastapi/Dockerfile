FROM python:3.11-slim

WORKDIR /fastapi

# Установим зависимости
RUN apt-get update \
 && apt-get install -y netcat-openbsd ffmpeg \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
