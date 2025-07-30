from fastapi import APIRouter

router = APIRouter(prefix="/rules", tags=["Staff - Rules"])


@router.get("/", summary="列出所有規則")
async def list_rules():
    return {"message": "list rules"} 