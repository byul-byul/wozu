# fastapi/app/user/models.py

# Why it's needed: Defines the User model, used for authentication and user data across the app.
# Why it's named that way: models.py holds SQLAlchemy models related to the user module.
# What it does: Declares the User table with fields like email, phone, password hash, verification status.

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.core.models import BaseDBModel
from typing import Optional
from uuid import UUID

class User(BaseDBModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    full_name = Column(String, nullable=True)
    nick_name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    last_login_at = Column(DateTime, nullable=True)

    photo_url = Column(String, nullable=True)
    company_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("companies.id"), nullable=True)
    company: Mapped[Optional["Company"]] = relationship(back_populates="users")

    is_email_verified = Column(Boolean, default=False, nullable=False)
    is_phone_verified = Column(Boolean, default=False, nullable=False)

    email_tokens = relationship("EmailToken", back_populates="user", cascade="all, delete")
