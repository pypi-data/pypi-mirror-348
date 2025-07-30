from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User as UserModel
from app.schemas.token import Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/staff/auth/login")

router = APIRouter(prefix="/auth", tags=["Staff - Auth"])


@router.post("/login", response_model=Token, summary="員工登入並取得 Token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm 使用 username 欄位，這裡視為 email
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="帳號或密碼錯誤")

    token = create_access_token(user.id)
    return Token(access_token=token) 