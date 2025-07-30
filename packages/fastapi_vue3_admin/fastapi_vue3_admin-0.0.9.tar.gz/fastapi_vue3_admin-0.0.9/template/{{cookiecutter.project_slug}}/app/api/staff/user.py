from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_password_hash, get_current_user
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["Staff - Users"])


@router.get("/", response_model=List[UserRead], summary="列出所有員工")
async def list_users(db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    users = db.query(UserModel).all()
    return users


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="新增員工")
async def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(UserModel.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email 已存在")

    user_obj = UserModel(name=user_in.name, email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj 