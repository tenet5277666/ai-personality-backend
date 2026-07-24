from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from core.database import get_db
from db.models import PersonalityBase, PersonalityWVW, PersonalityEmotion, EmotionSample, SocialTrain

personality_router = APIRouter()


# ====================== 三观管理 ======================
@personality_router.get("/wvw/get")
def get_wvw(avatar_id: int, db: Session = Depends(get_db)):
    wvw = db.query(PersonalityWVW).filter(PersonalityWVW.avatar_id == avatar_id).first()
    if not wvw:
        return {"code": 200, "data": {}}
    return {"code": 200, "data": {"world_view": wvw.world_view, "life_view": wvw.life_view,
            "value_view": wvw.value_view, "is_init_constellation": wvw.is_init_constellation}}


class UpdateWVWRequest(BaseModel):
    avatar_id: int
    world_view: str = ""
    life_view: str = ""
    value_view: str = ""


@personality_router.post("/wvw/update")
def update_wvw(req: UpdateWVWRequest, db: Session = Depends(get_db)):
    wvw = db.query(PersonalityWVW).filter(PersonalityWVW.avatar_id == req.avatar_id).first()
    if not wvw:
        wvw = PersonalityWVW(avatar_id=req.avatar_id)
        db.add(wvw)
    if req.world_view:
        wvw.world_view = req.world_view
    if req.life_view:
        wvw.life_view = req.life_view
    if req.value_view:
        wvw.value_view = req.value_view
    wvw.is_init_constellation = 0
    db.commit()
    return {"code": 200, "msg": "三观更新成功"}


# ====================== 基础人设管理 ======================
class UpdateBaseRequest(BaseModel):
    avatar_id: int
    age: str = ""
    identity: str = ""
    talk_speed: str = "normal"
    hobby: str = ""
    taboo: str = ""
    advantage: str = ""
    disadvantage: str = ""


@personality_router.get("/base/get")
def get_base(avatar_id: int, db: Session = Depends(get_db)):
    base = db.query(PersonalityBase).filter(PersonalityBase.avatar_id == avatar_id).first()
    if not base:
        return {"code": 200, "data": {}}
    return {"code": 200, "data": {"age": base.age, "identity": base.identity,
            "talk_speed": base.talk_speed, "hobby": base.hobby, "taboo": base.taboo,
            "advantage": base.advantage, "disadvantage": base.disadvantage}}


@personality_router.post("/base/update")
def update_base(req: UpdateBaseRequest, db: Session = Depends(get_db)):
    base = db.query(PersonalityBase).filter(PersonalityBase.avatar_id == req.avatar_id).first()
    if not base:
        base = PersonalityBase(avatar_id=req.avatar_id)
        db.add(base)
    if req.age:
        base.age = req.age
    if req.identity:
        base.identity = req.identity
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
    return {"code": 200, "msg": "基础人设更新成功"}


# ====================== 情绪训练 ======================
@personality_router.get("/emotion/list")
def get_emotion(avatar_id: int, db: Session = Depends(get_db)):
    emotions = db.query(PersonalityEmotion).filter(PersonalityEmotion.avatar_id == avatar_id).all()
    data = [{"id": e.id, "emotion_type": e.emotion_type, "trigger_rule": e.trigger_rule,
             "feature": e.feature, "intensity": e.intensity} for e in emotions]
    return {"code": 200, "data": data}


class SaveEmotionRequest(BaseModel):
    avatar_id: int
    emotion_type: str
    trigger_rule: str = ""
    feature: str = ""
    intensity: int = 5


@personality_router.post("/emotion/save")
def save_emotion(req: SaveEmotionRequest, db: Session = Depends(get_db)):
    existing = db.query(PersonalityEmotion).filter(
        PersonalityEmotion.avatar_id == req.avatar_id,
        PersonalityEmotion.emotion_type == req.emotion_type
    ).first()
    if existing:
        existing.trigger_rule = req.trigger_rule
        existing.feature = req.feature
        existing.intensity = req.intensity
    else:
        new_e = PersonalityEmotion(avatar_id=req.avatar_id, emotion_type=req.emotion_type,
                                    trigger_rule=req.trigger_rule, feature=req.feature,
                                    intensity=req.intensity)
        db.add(new_e)
    db.commit()
    return {"code": 200, "msg": "情绪配置已保存"}


class AddSampleRequest(BaseModel):
    avatar_id: int
    emotion_type: str
    content: str


@personality_router.post("/emotion/sample/add")
def add_emotion_sample(req: AddSampleRequest, db: Session = Depends(get_db)):
    sample = EmotionSample(avatar_id=req.avatar_id, emotion_type=req.emotion_type, content=req.content)
    db.add(sample)
    db.commit()
    return {"code": 200, "msg": "情绪样本已保存"}


# ====================== 社交训练 ======================
@personality_router.get("/social/list")
def get_social(avatar_id: int, db: Session = Depends(get_db)):
    socials = db.query(SocialTrain).filter(SocialTrain.avatar_id == avatar_id).all()
    data = [{"id": s.id, "social_type": s.social_type, "social_feature": s.social_feature} for s in socials]
    return {"code": 200, "data": data}


class SaveSocialRequest(BaseModel):
    avatar_id: int
    social_type: str
    social_feature: str = ""


@personality_router.post("/social/save")
def save_social(req: SaveSocialRequest, db: Session = Depends(get_db)):
    existing = db.query(SocialTrain).filter(
        SocialTrain.avatar_id == req.avatar_id,
        SocialTrain.social_type == req.social_type
    ).first()
    if existing:
        existing.social_feature = req.social_feature
    else:
        new_s = SocialTrain(avatar_id=req.avatar_id, social_type=req.social_type,
                            social_feature=req.social_feature)
        db.add(new_s)
    db.commit()
    return {"code": 200, "msg": "社交训练配置已保存"}
