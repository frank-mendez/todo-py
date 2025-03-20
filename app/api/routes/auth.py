from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.api.errors import UnauthorizedError, ValidationError
from app.core.security import create_access_token, verify_password
from app.core.config import settings
from app.crud import user
from app.api.dependencies import get_db
from app.schemas.user import User, UserInDB

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")  # Remove API version prefix since it's handled by the main router

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Get current user from token."""
    try:
        current_user = user.get_user_by_token(db, token)
        if not current_user:
            raise UnauthorizedError("Invalid authentication credentials")
        return current_user
    except Exception as e:
        raise UnauthorizedError("Could not validate credentials")

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Check if current user is active."""
    if current_user.disabled:
        raise ValidationError("Inactive user")
    return current_user

@router.post("/token")
async def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Login endpoint to get access token."""
    current_user = user.authenticate(
        db, 
        username=form_data.username, 
        password=form_data.password
    )
    if not current_user:
        raise UnauthorizedError("Incorrect username or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": current_user.username},  # Fixed: use current_user instead of user
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/users/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile."""
    return current_user
