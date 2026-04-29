import os
import smtplib
from email.message import EmailMessage


def send_verification_email(email: str, token: str):
    frontend_verify_url = os.getenv("FRONTEND_VERIFY_URL", "http://localhost:3001/verify")
    verify_link = f"{frontend_verify_url}?token={token}"
    smtp_host = os.getenv("SMTP_HOST","smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    smtp_from = os.getenv("SMTP_FROM", smtp_user or "no-reply@jobpilot.local")

    # Dev fallback: keep local flow working without SMTP credentials.
    if not smtp_host or not smtp_user or not smtp_password:
        print(f"[EMAIL NOT SENT] Verification link for {email}: {verify_link}")
        return
    message = EmailMessage()
    message["Subject"] = "Verify your JobPilot account"
    message["From"] = smtp_from
    message["To"] = email
    message.set_content(
        "Welcome to JobPilot!\n\n"
        "Please verify your account using this link:\n"
        f"{verify_link}\n\n"
        "If you did not create this account, you can ignore this email."
    )

    with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)
