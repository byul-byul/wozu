# app/users/models.py

# Why it's needed: Defines the User model, which is a core database table used across the app.
# Why it's named that way: Follows common convention — models.py holds SQLAlchemy models related to this module.
# What it does: Declares the User table with fields like email, password hash, and active status.

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    email_tokens = relationship("EmailToken", back_populates="user", cascade="all, delete")
