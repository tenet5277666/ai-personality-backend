from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
from db.models import PersonalityBase, PersonalityWVW, PersonalityEmotion, SocialTrain
from rag.vector_core import insert_rag_sample, clear_avatar_rag

admin_router = APIRouter()


class SetBaseRequest(BaseModel):
    avatar_id: int
    age: str = ""
    identity: str = ""
    talk_speed: str = "normal"
    hobby: str = ""
    taboo: str = ""
    advantage: str = ""
    disadvantage: str = ""


@admin_router.post("/set_base_personality")
def admin_set_base_personality(req: SetBaseRequest, db: Session = Depends(get_db)):
    """后台手动设置/覆盖基础人设"""
    base = db.query(PersonalityBase).filter(PersonalityBase.avatar_id == req.avatar_id).first()
    if not base:
        base = PersonalityBase(avatar_id=req.avatar_id)
        db.add(base)
    if req.age:
        base.age = req.age
    if req.identity:
        base.identity = req.identity
    if req.talk_speed:
        base.talk_speed = req.talk_speed
    if req.hobby:
        base.hobby = req.hobby
    if req.taboo:
        base.taboo = req.taboo
    if req.advantage:
        base.advantage = req.advantage
    if req.disadvantage:
        base.disadvantage = req.disadvantage
    db.commit()
    return {"code": 200, "msg": "【后台】基础人设更新成功"}


class SetWVWRequest(BaseModel):
    avatar_id: int
    world_view: str
    life_view: str
    value_view: str


@admin_router.post("/set_wvw")
def admin_set_wvw(req: SetWVWRequest, db: Session = Depends(get_db)):
    """后台强制覆盖三观"""
    wvw = db.query(PersonalityWVW).filter(PersonalityWVW.avatar_id == req.avatar_id).first()
    if not wvw:
        wvw = PersonalityWVW(avatar_id=req.avatar_id, is_init_constellation=0)
        db.add(wvw)
    wvw.world_view = req.world_view
    wvw.life_view = req.life_view
    wvw.value_view = req.value_view
    wvw.is_init_constellation = 0
    db.commit()
    return {"code": 200, "msg": "【后台】三观强制覆盖成功，已变为自定义人格内核"}


class FeedRagRequest(BaseModel):
    avatar_id: int
    emotion_type: str
    social_type: str
    content: str
    weight: int = 10


@admin_router.post("/feed_rag_sample")
def admin_feed_rag_sample(req: FeedRagRequest, db: Session = Depends(get_db)):
    """后台手动喂高权重数据"""
    insert_rag_sample(user_id=req.avatar_id, avatar_id=req.avatar_id,
                      emotion_type=req.emotion_type, social_type=req.social_type,
                      content=req.content, weight=req.weight)
    return {"code": 200, "msg": f"【后台】成功投喂高权重训练样本，权重:{req.weight}"}


class AvatarIdRequest(BaseModel):
    avatar_id: int


@admin_router.post("/clear_rag")
def admin_clear_rag(req: AvatarIdRequest):
    """后台清空该分身所有RAG训练数据"""
    clear_avatar_rag(req.avatar_id)
    return {"code": 200, "msg": "【后台】该分身RAG训练数据已清空"}


@admin_router.get("/get_all_personality")
def admin_get_all_personality(avatar_id: int, db: Session = Depends(get_db)):
    """后台调试：查看完整人设数据"""
    base = db.query(PersonalityBase).filter(PersonalityBase.avatar_id == avatar_id).first()
    wvw = db.query(PersonalityWVW).filter(PersonalityWVW.avatar_id == avatar_id).first()
    emotion_list = db.query(PersonalityEmotion).filter(PersonalityEmotion.avatar_id == avatar_id).all()
    social_list = db.query(SocialTrain).filter(SocialTrain.avatar_id == avatar_id).all()

    def safe_dict(obj):
        if not obj:
            return {}
        return {k: str(v) for k, v in obj.__dict__.items() if not k.startswith("_")}

    return {
        "code": 200, "data": {
            "base_personality": safe_dict(base),
            "wvw": safe_dict(wvw),
            "emotion_config": [safe_dict(e) for e in emotion_list],
            "social_config": [safe_dict(s) for s in social_list]
        }
    }


@admin_router.post("/reset_personality")
def admin_reset_personality(req: AvatarIdRequest, db: Session = Depends(get_db)):
    """后台一键重置该分身所有后天训练数据"""
    db.query(PersonalityBase).filter(PersonalityBase.avatar_id == req.avatar_id).delete()
    db.query(PersonalityEmotion).filter(PersonalityEmotion.avatar_id == req.avatar_id).delete()
    db.query(SocialTrain).filter(SocialTrain.avatar_id == req.avatar_id).delete()
    db.commit()
    clear_avatar_rag(req.avatar_id)
    return {"code": 200, "msg": "【后台】人设后天训练数据已全部重置，保留星座初始三观"}
