from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.api.errors import UnauthorizedError, ValidationError
from app.core.security import create_access_token
from app.core.config import settings
from app.crud import user
from app.api.dependencies import get_db
from app.schemas.user import User
from app.schemas.token import Token

router = APIRouter(tags=["auth"])  # Remove prefix here since it's handled by main router

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")  # Add full path

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
    if not current_user.is_active:  # Changed from disabled to is_active
        raise ValidationError("Inactive user")
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_obj = user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_obj.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user profile."""
    return current_user
