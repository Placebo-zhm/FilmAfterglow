from fastapi import APIRouter

from app.api.admin.router import router as admin_router
from app.api.public.router import router as public_router

api_router = APIRouter()
api_router.include_router(public_router)
api_router.include_router(admin_router, prefix="/admin")
