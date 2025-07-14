# fastapi/app/main.py

# Why it's needed: Entry point for launching the FastAPI application.
# Why it's named that way: `main.py` is the conventional name for the main execution file in Python apps.
# What it does: Creates the FastAPI app, includes routers, and runs the Uvicorn server.

from fastapi import FastAPI
from app.auth.routes import router as auth_router

app = FastAPI()

app.include_router(auth_router)
