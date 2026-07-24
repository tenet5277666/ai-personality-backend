from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
from core.database import get_db
from core.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from db.models import User

user_router = APIRouter()


class LoginRequest(BaseModel):
    phone: str


def create_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@user_router.post("/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """手机号登录/注册"""
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user:
        user = User(phone=req.phone)
        db.add(user)
        db.commit()
        db.refresh(user)
    token = create_token(user.id)
    return {"code": 200, "data": {"token": token, "user_id": user.id, "phone": req.phone}}


@user_router.get("/profile")
def profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {
        "code": 200,
        "data": {
            "id": user.id,
            "phone": user.phone,
            "avatar": user.avatar,
            "create_time": str(user.create_time)
        }
    }
