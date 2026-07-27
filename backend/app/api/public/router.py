from fastapi import APIRouter

from app.api.public import health

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["public-health"])
