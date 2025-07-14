# fastapi/app/auth/security.py

# зачем нужен: содержит функции для безопасной работы с паролями и JWT-токенами.
# почему так называется: security.py — общее название для всех механизмов безопасности, связанных с auth.
# что делает: хеширует пароли, проверяет их, создаёт и декодирует JWT-токены.

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "secret"  # TODO: заменить на os.getenv
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
