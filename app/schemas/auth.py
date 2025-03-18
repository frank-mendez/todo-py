from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload data"""
    username: str | None = None


class UserAuth(BaseModel):
    """Schema for user authentication"""
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Schema for detailed token response"""
    access_token: str
    token_type: str
    expires_in: int
    user_id: int
    username: str