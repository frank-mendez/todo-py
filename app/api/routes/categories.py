from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from app.api.routes.auth import get_current_active_user
from app.api.errors import NotFoundError, ValidationError

router = APIRouter()

class CategoryBase(BaseModel):
    name: str
    description: str = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    owner: str

    class Config:
        orm_mode = True

# Temporary in-memory storage
categories_db = {}
category_id_counter = 1

@router.post("/categories/", response_model=Category)
async def create_category(
    category: CategoryCreate,
    current_user: dict = Depends(get_current_active_user)
):
    global category_id_counter
    new_category = Category(
        id=category_id_counter,
        **category.dict(),
        owner=current_user.username
    )
    categories_db[category_id_counter] = new_category
    category_id_counter += 1
    return new_category

@router.get("/categories/", response_model=List[Category])
async def get_categories(current_user: dict = Depends(get_current_active_user)):
    return [cat for cat in categories_db.values() if cat.owner == current_user.username]

@router.get("/categories/{category_id}", response_model=Category)
async def get_category(
    category_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if category_id not in categories_db:
        raise NotFoundError("Category not found")
    category = categories_db[category_id]
    if category.owner != current_user.username:
        raise NotFoundError("Category not found")
    return category

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(
    category_id: int,
    category_update: CategoryCreate,
    current_user: dict = Depends(get_current_active_user)
):
    if category_id not in categories_db:
        raise NotFoundError("Category not found")
    category = categories_db[category_id]
    if category.owner != current_user.username:
        raise NotFoundError("Category not found")
    
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    categories_db[category_id] = category
    return category

@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    current_user: dict = Depends(get_current_active_user)
):
    if category_id not in categories_db:
        raise NotFoundError("Category not found")
    category = categories_db[category_id]
    if category.owner != current_user.username:
        raise NotFoundError("Category not found")
    
    del categories_db[category_id]
    return {"message": "Category deleted successfully"}
