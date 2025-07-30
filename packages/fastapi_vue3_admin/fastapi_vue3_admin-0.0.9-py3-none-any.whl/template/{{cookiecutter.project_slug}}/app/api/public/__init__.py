from fastapi import APIRouter

from . import endpoint1

router = APIRouter(prefix="/public")
router.include_router(endpoint1.router) 