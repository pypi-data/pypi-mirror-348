from fastapi import APIRouter

router = APIRouter(prefix="/hello", tags=["Public"])


@router.get("/", summary="公開 Hello World")
async def public_hello():
    return {"message": "Hello, world!"} 