from datetime import datetime, timedelta
from typing import Optional, Any
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from app.core.config import settings

load_dotenv()

# Security configuration
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")  # Updated token URL

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None

def get_token_data(token: str) -> Optional[str]:
    """Extract username from token."""
    payload = verify_token(token)
    if payload is None:
        return None
    username: str = payload.get("sub")
    return username