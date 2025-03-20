from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api.routes.auth import get_current_active_user
from app.api.dependencies import get_db
from app.core.security import get_password_hash
from app.crud.user import user as crud_user  # Updated import
from app.schemas.user import User, UserCreate, UserUpdate
from app.api.errors import NotFoundError, ValidationError, ConflictError

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_new_user(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """Create new user."""
    # Check if user with this email exists
    if crud_user.get_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        user = crud_user.create(db, obj_in=user_in)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/users/", response_model=List[User])
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100
):
    """Get list of users."""
    users = crud_user.get_multi(db, skip=skip, limit=limit)
    return users

@router.put("/users/me", response_model=User)
async def update_current_user(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update current user."""
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    if not user:
        raise NotFoundError("User not found")
    return user

@router.delete("/users/me")
async def delete_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete current user."""
    success = crud_user.remove(db, id=current_user.id)
    if not success:
        raise NotFoundError("User not found")
    return {"message": "User deleted successfully"}

@router.post("/users/me/disable")
async def disable_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Disable current user."""
    user = crud_user.update(db, db_obj=current_user, obj_in=UserUpdate(disabled=True))
    if not user:
        raise NotFoundError("User not found")
    return {"message": "User disabled successfully"}
