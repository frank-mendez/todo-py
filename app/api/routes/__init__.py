from fastapi import APIRouter
from app.api.routes import auth, users, tasks, categories

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(categories.router, tags=["categories"])
api_router.include_router(tasks.router, tags=["tasks"])
