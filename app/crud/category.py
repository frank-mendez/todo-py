from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.core.logging import get_logger

logger = get_logger(__name__)

def create_category(db: Session, category: CategoryCreate, user_id: int) -> Category:
    """Create a new category."""
    db_category = Category(
        **category.dict(),
        owner_id=user_id
    )
    db.add(db_category)
    try:
        db.commit()
        db.refresh(db_category)
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating category: {str(e)}")
        raise
    return db_category

def get_category(db: Session, category_id: int, user_id: int) -> Optional[Category]:
    """Get a category by ID and owner."""
    return db.query(Category).filter(
        Category.id == category_id,
        Category.owner_id == user_id
    ).first()

def get_categories(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100
) -> List[Category]:
    """Get list of categories for a user."""
    return db.query(Category)\
        .filter(Category.owner_id == user_id)\
        .offset(skip)\
        .limit(limit)\
        .all()

def update_category(
    db: Session,
    category_id: int,
    category: CategoryUpdate,
    user_id: int
) -> Optional[Category]:
    """Update category details."""
    db_category = get_category(db, category_id, user_id)
    if not db_category:
        return None
    
    update_data = category.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_category, field, value)
    
    try:
        db.commit()
        db.refresh(db_category)
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating category: {str(e)}")
        raise
    return db_category

def delete_category(db: Session, category_id: int, user_id: int) -> bool:
    """Delete a category."""
    db_category = get_category(db, category_id, user_id)
    if not db_category:
        return False
    
    try:
        db.delete(db_category)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting category: {str(e)}")
        raise
    return True

def get_category_by_name(
    db: Session,
    name: str,
    user_id: int
) -> Optional[Category]:
    """Get a category by name and owner."""
    return db.query(Category).filter(
        Category.name == name,
        Category.owner_id == user_id
    ).first()
