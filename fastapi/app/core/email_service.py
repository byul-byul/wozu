# fastapi/app/core/email_service.py

# зачем нужен: отправка email через Brevo API (вместо SMTP)
# почему так называется: email_service — единая точка для отправки писем в WOZU
# что делает: отправляет письмо по API, логирует ответ

import os
import httpx
import logging

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BASE_URL = os.getenv("EMAIL_VERIFICATION_BASE_URL")  # ← берём из .env актуальный base URL

async def send_verification_email(to_email: str, token: str):
    data = {
        "sender": {"name": "WOZU", "email": "burhan.hajili@gmail.com"},  # ← подтверждённый sender!
        "to": [{"email": to_email}],
        "subject": "WOZU — Email Verification",
        "htmlContent": f"""
        <p>Hi!</p>
        <p>Please verify your email by clicking the link below:</p>
        <a href="{BASE_URL}/auth/verify-email?token={token}">Verify Email</a>  <!-- добавлен /auth -->
        """,
    }
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(BREVO_API_URL, json=data, headers=headers)
        response.raise_for_status()
        logging.info("Email sent to %s (status %s)", to_email, response.status_code)
