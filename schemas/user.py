from pydantic import BaseModel, EmailStr , Field


class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8 , max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel): 
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    username: str


class ResetPasswordRequest(BaseModel):
    token : str
    new_password: str = Field(..., min_length=8, max_length=128)