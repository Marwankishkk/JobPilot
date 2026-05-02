import os
import smtplib
from email.message import EmailMessage

smtp_host = os.getenv("SMTP_HOST","smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", "587"))
smtp_user = os.getenv("SMTP_USER")
smtp_password = os.getenv("SMTP_PASSWORD")
smtp_from = os.getenv("SMTP_FROM", smtp_user or "no-reply@jobpilot.local")
def send_verification_email(email: str, token: str):
    frontend_verify_url = os.getenv("FRONTEND_URL", "http://localhost:3001/verify")
    frontend_verify_url = f"{frontend_verify_url}/verify" if not frontend_verify_url.endswith("/verify") else frontend_verify_url
    verify_link = f"{frontend_verify_url}?token={token}"
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

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=80) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)
    except Exception as e:
        print("SMTP ERROR:", e)

def send_reset_password_mail(email: str, token: str):
    reset_base = os.getenv("FRONTEND_URL", "http://localhost:3001/reset-password")
    reset_base = f"{reset_base}/reset-password" if not reset_base.endswith("/reset-password") else reset_base
    reset_link = f"{reset_base}?token={token}"
    # Dev fallback: keep local flow working without SMTP credentials.
    if not smtp_host or not smtp_user or not smtp_password:
        print(f"[EMAIL NOT SENT] Password reset link for {email}: {reset_link}")
        return
    message = EmailMessage()
    message["Subject"] = "Reset your JobPilot password"
    message["From"] = smtp_from
    message["To"] = email
    message.set_content(
        "You requested a password reset for your JobPilot account.\n\n"
        "Use this link to set a new password (it expires in one hour):\n"
        f"{reset_link}\n\n"
        "If you did not request this, you can ignore this email."
    )
    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=80) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)
    except Exception as e:
        print("SMTP ERROR:", e)
