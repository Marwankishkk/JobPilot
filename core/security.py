from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")

    if not secret_key:
        raise ValueError("SECRET_KEY is missing")

    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=15))
    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": "access",
    })
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def create_refresh_token(data: dict):
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")

    if not secret_key:
        raise ValueError("SECRET_KEY is missing")

    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(days=7)
    to_encode.update({
        "exp": expire,
        "iat": now,
        "type": "refresh",
    })
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)

def decode_access_token(token: str):
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")

    if not secret_key:
        raise ValueError("SECRET_KEY is missing")

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def decode_refresh_token(token: str):
    payload = decode_access_token(token)
    if payload.get("type") != "refresh":
        raise ValueError("Invalid token type")
    return payload
    
