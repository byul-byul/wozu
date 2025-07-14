# fastapi/app/auth/email_utils.py

# зачем нужен: обеспечивает отправку писем для подтверждения email и других целей.
# почему так называется: email_utils.py — логичное имя для утилит, связанных с отправкой почты.
# что делает: формирует тело письма, создаёт ссылку подтверждения, отправляет письмо через SMTP.

import smtplib
from email.message import EmailMessage

def send_verification_email(to_email: str, token: str):
    msg = EmailMessage()
    msg["Subject"] = "WOZU — Подтверждение email"
    msg["From"] = "noreply@wozu.app"
    msg["To"] = to_email
    msg.set_content(f"Перейдите по ссылке для подтверждения: https://wozu.app/verify-email?token={token}")

    # Пример SMTP (замени на реальный SMTP-сервер)
    with smtplib.SMTP("localhost", 1025) as smtp:
        smtp.send_message(msg)
