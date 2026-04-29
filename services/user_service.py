from sqlalchemy.orm import Session
from datetime import timedelta
from schemas.user import UserCreate , UserLogin
from models.user import User
from core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    create_refresh_token,
    decode_refresh_token,
)
from repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def get_current_user(self, token: str):
        try:
            payload = decode_access_token(token)
            if payload.get("type") != "access":
                raise ValueError("Invalid token type")
            email = payload.get("sub")
            if email is None:
                raise ValueError("Invalid token")
            return email
        except ValueError as e:
            raise ValueError(str(e))
        
    
    def register_user(self, db: Session, user_data: UserCreate):

        # check if email exists
        existing = self.repo.get_by_email(db, user_data.email)
        if existing:
            raise ValueError("Email already registered")
        # create user
        new_user = User(
            email=user_data.email,
            hashed_password=hash_password(user_data.password)
        )

        return self.repo.create(db, new_user)
    
    def login(self, db: Session, user_data: UserLogin):
        user = self.repo.get_by_email(db, user_data.email)

        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(user_data.password, user.hashed_password):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=30)
        )
        refresh_token = create_refresh_token(
            data={"sub": user.email}
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, refresh_token: str):
        payload = decode_refresh_token(refresh_token)
        email = payload.get("sub")
        if email is None:
            raise ValueError("Invalid token")

        access_token = create_access_token(
            data={"sub": email},
            expires_delta=timedelta(minutes=30),
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    
    