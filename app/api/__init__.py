from fastapi import APIRouter
from app.api.routes import api_router
from app.core.config import settings

router = APIRouter()

# Include the API router with version prefix only (removed duplicate /api)
router.include_router(api_router, prefix=settings.API_V1_STR)

__all__ = ["router"]
