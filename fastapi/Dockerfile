FROM python:3.11-slim

WORKDIR /fastapi

# Установим netcat
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
