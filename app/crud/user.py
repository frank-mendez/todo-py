from typing import Optional, List
from sqlalchemy.orm import Session
from jose import jwt
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.logging import get_logger
from app.crud.base import CRUDBase

logger = get_logger(__name__)

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create a new user with hashed password."""
        # Check for existing user first
        if self.get_by_email(db, email=obj_in.email):
            raise ValueError("Email already registered")
            
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            full_name=obj_in.full_name,
            hashed_password=get_password_hash(obj_in.password),
            is_active=True  # Changed from disabled=False
        )
        
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating user: {str(e)}")
            raise

    def is_active(self, user: User) -> bool:
        """Check if user is active."""
        return user.is_active  # Changed from not user.disabled

    def get_user_by_token(self, db: Session, token: str) -> Optional[User]:
        """Get user by JWT token."""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]  # Changed from ALGORITHM to JWT_ALGORITHM
            )
            username: str = payload.get("sub")
            if username is None:
                return None
            return self.get_by_username(db, username=username)
        except jwt.JWTError:
            return None

# Create single instance of CRUDUser
user = CRUDUser(User)

# Export everything needed
__all__ = [
    'user',
    'User',
    'UserCreate',
    'UserUpdate'
]
