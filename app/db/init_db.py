from sqlalchemy.orm import Session
from app.core.config import settings
from app.crud import user, create_category
from app.schemas.user import UserCreate
from app.schemas.category import CategoryCreate
from app.core.logging import get_logger
from app.db.base import Base
from app.db.session import engine
from app.models.user import User  # Add this import

logger = get_logger(__name__)

# Initial data for database seeding
FIRST_SUPERUSER = {
    "email": "admin@example.com",
    "password": "Admin123!",  # Updated to meet password requirements
    "username": "admin",
    "full_name": "Initial Admin"
}

INITIAL_CATEGORIES = [
    {"name": "Work", "description": "Work related tasks"},
    {"name": "Personal", "description": "Personal tasks"},
    {"name": "Shopping", "description": "Shopping list"},
]

def init_db(db: Session) -> None:
    """Initialize database with required tables and initial data."""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Created database tables")

        # Check if we should seed the database
        user = create_first_superuser(db)
        if user:
            create_initial_categories(db, user.id)
            logger.info("Database seeded successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def create_first_superuser(db: Session):
    """Create the first superuser if it doesn't exist."""
    try:
        superuser = user.get_by_email(db, email=FIRST_SUPERUSER["email"])
        if not superuser:
            user_in = UserCreate(
                email=FIRST_SUPERUSER["email"],
                password=FIRST_SUPERUSER["password"],
                username=FIRST_SUPERUSER["username"],
                full_name=FIRST_SUPERUSER["full_name"]
            )
            superuser = user.create(db, obj_in=user_in)
            logger.info(f"Created first superuser: {superuser.email}")
            return superuser
        return None
    except Exception as e:
        logger.error(f"Error creating superuser: {str(e)}")
        raise

def create_initial_categories(db: Session, user_id: int):
    """Create initial categories if they don't exist."""
    try:
        for category_data in INITIAL_CATEGORIES:
            category_in = CategoryCreate(**category_data)
            category = create_category(db, category_in, user_id)
            logger.info(f"Created initial category: {category.name}")
    except Exception as e:
        logger.error(f"Error creating initial categories: {str(e)}")
        raise

def reset_db() -> None:
    """Reset database (for development purposes only)."""
    try:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        logger.warning("Database has been reset")
    except Exception as e:
        logger.error(f"Error resetting database: {str(e)}")
        raise

if __name__ == "__main__":
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        logger.info("Creating initial data")
        init_db(db)
        logger.info("Initial data created")
    except Exception as e:
        logger.error(f"Error creating initial data: {str(e)}")
        raise
    finally:
        db.close()
