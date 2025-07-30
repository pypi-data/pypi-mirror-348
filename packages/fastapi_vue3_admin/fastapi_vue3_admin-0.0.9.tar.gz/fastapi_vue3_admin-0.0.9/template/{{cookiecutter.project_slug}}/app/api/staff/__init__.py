from fastapi import APIRouter

from . import user, rules, auth

router = APIRouter(prefix="/staff")
router.include_router(user.router)
router.include_router(rules.router)
router.include_router(auth.router) 