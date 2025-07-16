#!/bin/bash
# wait-for-postgres.sh like logic
echo "⏳ Waiting for Postgres..."
while ! nc -z db 5432; do
  sleep 0.5
done

echo "✅ Postgres is up. Running Alembic migrations..."
alembic upgrade head

echo "🚀 Starting Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
