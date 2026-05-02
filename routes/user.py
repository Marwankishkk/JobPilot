from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session

from schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from services.user_service import UserService
from core.db import get_db

router = APIRouter(prefix="/users", tags=["Users"])

service = UserService()


# ----------------------------
# REGISTER
# ----------------------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return service.register_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
#-----------------------------
#VERIFY User
#-----------------------------
@router.get("/verify")
def verify_account(token: str, db: Session = Depends(get_db)):
    try:
        user = service.verify_account(token, db)
        if user:
            return {"message": "Account verified successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid or expired token")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# ----------------------------
# LOGIN (set cookies)
# ----------------------------
@router.post("/login")
def login(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    try:
        tokens = service.login(db, user)

        # Access token cookie
        response.set_cookie(
            key="access_token",
            value=tokens["access_token"],
            httponly=True,
            secure=False,  # True in production (HTTPS)
            samesite="lax",
            max_age=60 * 30,
            path="/",
        )
        # Refresh token cookie
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,
            path="/",
        )

        return {"message": "login successful"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_current_user_email(request: Request):
    token = request.cookies.get("access_token")
    print("Access token from cookie:", token)  # Debugging line
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        return service.get_current_user(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# ----------------------------
# FORGOT PASSWORD
# ----------------------------
@router.post("/forgot-password")
def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    try:
        return service.forget_password(body.email, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------
# RESET PASSWORD
# ----------------------------
@router.post("/reset-password")
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        return service.reset_password(body.token, db, body.new_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ----------------------------
# GET CURRENT USER (/me)
# ----------------------------
@router.get("/me")
def get_current_user(email: str = Depends(get_current_user_email)):
    return {"email": email}


# ----------------------------
# REFRESH TOKEN
# ----------------------------
@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    try:
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise HTTPException(status_code=401, detail="No refresh token")

        tokens = service.refresh_access_token(refresh_token)

        # update access token cookie
        response.set_cookie(
            key="access_token",
            value=tokens["access_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 30,
            path="/",
        )

        return {"message": "token refreshed"}

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


# ----------------------------
# LOGOUT 
# ----------------------------
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return {"message": "logged out"}