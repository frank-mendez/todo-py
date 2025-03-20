from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import verify_token, get_token_data
from app.core.config import settings
from app.core.logging import get_logger
from app.api.errors import UnauthorizedError
from app.db.session import SessionLocal

logger = get_logger(__name__)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token"
)

# Database dependency
def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Validate access token and return current user.
    """
    try:
        username = get_token_data(token)
        if not username:
            raise UnauthorizedError("Could not validate credentials")
        return {"username": username}
    except Exception as e:
        logger.error(f"Token validation error: {str(e)}")
        raise UnauthorizedError("Could not validate credentials")

async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Get current active user.
    """
    return current_user

def get_token_header(x_token: str = Depends(oauth2_scheme)) -> str:
    """
    Dependency for token header validation.
    """
    return x_token

class RateLimiter:
    """
    Basic rate limiting implementation.
    Should be replaced with proper rate limiting in production.
    """
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        # In production, use Redis or similar for rate limiting
        self._requests = {}

    async def check_rate_limit(self, user_id: str) -> bool:
        """
        Check if user has exceeded rate limit.
        """
        # Implement proper rate limiting logic here
        return True

rate_limiter = RateLimiter()

async def check_rate_limit(
    current_user: dict = Depends(get_current_active_user)
) -> None:
    """
    Rate limiting dependency.
    """
    is_allowed = await rate_limiter.check_rate_limit(current_user["username"])
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )