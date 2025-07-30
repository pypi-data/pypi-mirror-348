from sqlalchemy import Column, Integer, String

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=128), nullable=False)
    email = Column(String(length=255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=255), nullable=False)  # 儲存雜湊密碼 