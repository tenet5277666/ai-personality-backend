from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
from db.models import UserAvatar, PersonalityWVW
from personality.constellation_wvw import get_constellation_wvw

avatar_router = APIRouter()


class CreateAvatarRequest(BaseModel):
    user_id: int
    avatar_name: str
    train_type: str
    birthday: str


@avatar_router.post("/create")
def create_avatar(req: CreateAvatarRequest, db: Session = Depends(get_db)):
    """创建AI分身"""
    wvw_data = get_constellation_wvw(req.birthday)
    constellation = wvw_data.get("constellation", "")

    avatar = UserAvatar(
        user_id=req.user_id,
        avatar_name=req.avatar_name,
        train_type=req.train_type,
        birthday=req.birthday,
        constellation=constellation
    )
    db.add(avatar)
    db.commit()
    db.refresh(avatar)

    if constellation:
        wvw = PersonalityWVW(
            avatar_id=avatar.id,
            is_init_constellation=1,
            world_view=wvw_data.get("world_view", ""),
            life_view=wvw_data.get("life_view", ""),
            value_view=wvw_data.get("value_view", "")
        )
        db.add(wvw)
        db.commit()

    return {
        "code": 200,
        "msg": "分身创建成功",
        "data": {
            "avatar_id": avatar.id,
            "constellation": constellation,
            "world_view": wvw_data.get("world_view", ""),
            "life_view": wvw_data.get("life_view", ""),
            "value_view": wvw_data.get("value_view", "")
        }
    }


@avatar_router.get("/list")
def list_avatars(user_id: int, db: Session = Depends(get_db)):
    avatars = db.query(UserAvatar).filter(UserAvatar.user_id == user_id).all()
    result = [
        {"id": a.id, "avatar_name": a.avatar_name, "train_type": a.train_type,
         "birthday": a.birthday, "constellation": a.constellation, "status": a.status,
         "create_time": str(a.create_time)}
        for a in avatars
    ]
    return {"code": 200, "data": result}


@avatar_router.get("/detail")
def avatar_detail(avatar_id: int, db: Session = Depends(get_db)):
    avatar = db.query(UserAvatar).filter(UserAvatar.id == avatar_id).first()
    if not avatar:
        return {"code": 404, "msg": "分身不存在"}
    return {
        "code": 200,
        "data": {"id": avatar.id, "avatar_name": avatar.avatar_name,
                 "train_type": avatar.train_type, "birthday": avatar.birthday,
                 "constellation": avatar.constellation, "status": avatar.status}
    }
