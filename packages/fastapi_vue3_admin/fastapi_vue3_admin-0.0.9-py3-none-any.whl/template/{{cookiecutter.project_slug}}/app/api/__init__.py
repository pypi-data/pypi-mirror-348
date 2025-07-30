from fastapi import APIRouter

from .staff import router as staff_router
from .public import router as public_router

api_router = APIRouter()
api_router.include_router(staff_router)
api_router.include_router(public_router) 