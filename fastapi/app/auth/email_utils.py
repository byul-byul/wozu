# # fastapi/app/auth/email_utils.py

# # зачем нужен: обеспечивает отправку писем для подтверждения email и других целей.
# # почему так называется: email_utils.py — логичное имя для утилит, связанных с отправкой почты.
# # что делает: формирует тело письма, создаёт ссылку подтверждения, отправляет письмо через SMTP.

# import smtplib
# from email.message import EmailMessage
# import os

# import logging

# # ...
# logging.warning("SMTP_USER: %s", os.getenv("SMTP_USER"))
# logging.warning("SMTP_PASSWORD: %s", os.getenv("SMTP_PASSWORD"))


# def send_verification_email(to_email: str, token: str):
#     msg = EmailMessage()
#     msg["Subject"] = "WOZU — Email Verification"
#     msg["From"] = os.getenv("SMTP_USER")  # теперь берётся из переменной окружения
#     msg["To"] = to_email
#     msg.set_content(f"Please click the link to verify your email:\nhttps://wozu.app/verify-email?token={token}")

#     with smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT"))) as smtp:
#         smtp.starttls()
#         smtp.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
#         smtp.send_message(msg)
