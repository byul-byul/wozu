# wozu

# Auth Module

## 📌 Назначение
Отвечает за регистрацию, вход и подтверждение email. В будущем — подтверждение по телефону.

## 📦 Используемые технологии
- FastAPI
- SQLAlchemy ORM
- Alembic (миграции)
- JWT (аутентификация)
- PostgreSQL
- Pydantic
- SMTP (email-уведомления)

## 🧱 Структура модуля
- `models.py` — ORM-модель EmailToken
- `schemas.py` — схемы запросов/ответов: RegisterRequest, LoginRequest, TokenResponse
- `routes.py` — эндпоинты: /register, /login, /verify-email
- `services.py` — логика регистрации, логина, токенов
- `crud.py` — работа с БД: создание токенов, поиск пользователей
- `security.py` — bcrypt, JWT (создание/проверка)
- `email_utils.py` — отправка писем

## 📤 Эндпоинты
- `POST /auth/register` — регистрация пользователя
- `POST /auth/login` — вход по email/паролю
- `GET /auth/verify-email?token=...` — подтверждение email

## 🚧 В планах
- Подтверждение телефона (SMS)
- Сброс пароля
- Ограничение частоты запросов (rate limiting)
