from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi import Request, HTTPException
from schemas.user import UserCreate, UserLogin
from models.user import User
from .email_service import send_verification_email
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    create_refresh_token,
    decode_refresh_token,
    create_email_token,
    decode_email_token,
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
        
        send_verification_email(user.email,token)
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
        if not user.is_active:
            raise ValueError("Account not activated. Please check your email.")
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise ValueError("Invalid email or password")

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