from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse,
    RefreshTokenRequest,
)
from services.user_service import UserService
from core.db import get_db

router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

service = UserService()


def get_current_user_email(token: str = Depends(oauth2_scheme)):
    try:
        return service.get_current_user(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return service.register_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        return service.login(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(payload: RefreshTokenRequest):
    try:
        return service.refresh_access_token(payload.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
@router.get("/me")
def get_current_user(email: str = Depends(get_current_user_email)):
    return {"email": email}