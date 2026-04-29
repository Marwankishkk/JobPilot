from pydantic import BaseModel, EmailStr , Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8 , max_length=128)


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel): 
    access_token: str
    refresh_token: str
    token_type: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str