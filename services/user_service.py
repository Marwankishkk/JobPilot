from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import Request, HTTPException
from schemas.user import UserCreate, UserLogin
from models.user import User
from .email_service import send_verification_email, send_reset_password_mail
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    create_refresh_token,
    decode_refresh_token,
    create_email_token,
    decode_email_token,
    create_password_reset_token,
    decode_password_reset_token,
)
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    # ----------------------------
    # AUTH: GET CURRENT USER
    # ----------------------------
    def get_current_user(self, token: str):
        payload = decode_access_token(token)

        if not payload:
            raise ValueError("Invalid token")

        if payload.get("type") != "access":
            raise ValueError("Invalid token type")

        email = payload.get("sub")
        if not email:
            raise ValueError("Invalid token payload")

        return email
   


    # ----------------------------
    # REGISTER
    # ----------------------------
    def register_user(self, db: Session, user_data: UserCreate):
        existing = self.repo.get_by_email(db, user_data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        new_user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )
        user=self.repo.create(db, new_user)
        if not user:
            raise ValueError("Failed to create user")
        token = create_email_token(email=user.email)
        try:
            send_verification_email(user.email,token)
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="User registered but failed to send verification email. Please try again later."
            )
        return {"message": "User registered successfully. Please check your email to verify your account."}
    # ----------------------------
    # ACTIVATE ACCOUNT
    # ----------------------------
    def verify_account(self,token: str, db: Session ):
        try:

            payload = decode_email_token(token)
            print("Decoded token payload:", payload)

            if payload["type"] != "verify":
                raise Exception()

            email = payload["sub"]

        except:
            raise HTTPException(400, "Invalid or expired token")

        user = self.repo.activate_account(db, email)

        if not user:
            raise HTTPException(404, "User not found")

        return user
    # ----------------------------
    # LOGIN
    # ----------------------------
    def login(self, db: Session, user_data: UserLogin):

        user = self.repo.get_by_email(db, user_data.email)
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise ValueError("Invalid email or password")
        if not user.is_active:
            raise ValueError("Account not activated. Please check your email.")

        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=30),
        )

        refresh_token = create_refresh_token(
            data={"sub": user.email},
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    # ----------------------------
    # Forget Password
    # ----------------------------

    def forget_password(self, email: str, db: Session):
        user = self.repo.get_by_email(db, email)
        if not user:
            return {"message": "If an account exists for this email, you will receive reset instructions."}

        token = create_password_reset_token(email=user.email)
        try:
            send_reset_password_mail(user.email, token)
        except:
            raise ValueError("Failed to send reset password email. Please try again later.")

        return {"message": "If an account exists for this email, you will receive reset instructions."}

    def reset_password(self, token: str, db: Session, new_password: str):
        try:
            payload = decode_password_reset_token(token)
        except ValueError as e:
            raise ValueError(str(e))

        email = payload.get("sub")
        user = self.repo.get_by_email(db, email)
        if not user:
            raise ValueError("User not found")

        self.repo.update_password(db, user, hash_password(new_password))
        return {"message": "Password updated"}



    # ----------------------------
    # REFRESH TOKEN
    # ----------------------------
    def refresh_access_token(self, refresh_token: str):

        payload = decode_refresh_token(refresh_token)

        if not payload:
            raise ValueError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        email = payload.get("sub")
        if not email:
            raise ValueError("Invalid token payload")

        new_access_token = create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=30),
        )

        return {
            "access_token": new_access_token,
            "refresh_token": refresh_token,  # reuse or rotate later
            "token_type": "bearer",
        }