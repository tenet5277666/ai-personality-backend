from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
from db.models import AiAutoChat
from personality.ai_auto_train import auto_gen_social_talk, save_auto_train_record, correct_train_record

train_router = APIRouter()


class GenTrainRequest(BaseModel):
    avatar_id: int
    emotion_type: str = "calm"


@train_router.post("/auto/gen")
def gen_auto_train(req: GenTrainRequest, db: Session = Depends(get_db)):
    scene, prompt = auto_gen_social_talk(req.emotion_type)
    return {"code": 200, "data": {"scene": scene, "prompt": prompt, "emotion_type": req.emotion_type}}


@train_router.get("/auto/records")
def auto_train_records(avatar_id: int, db: Session = Depends(get_db)):
    records = db.query(AiAutoChat).filter(AiAutoChat.avatar_id == avatar_id)\
        .order_by(AiAutoChat.create_time.desc()).limit(50).all()
    data = [{"id": r.id, "emotion_type": r.emotion_type, "social_type": r.social_type,
             "ai_content": r.ai_content, "user_correct_content": r.user_correct_content,
             "is_correct": r.is_correct, "weight": r.weight,
             "create_time": str(r.create_time)} for r in records]
    return {"code": 200, "data": data}


class CorrectRequest(BaseModel):
    record_id: int
    user_content: str


@train_router.post("/correct")
def correct_record(req: CorrectRequest, db: Session = Depends(get_db)):
    result = correct_train_record(db, req.record_id, req.user_content)
    if not result:
        return {"code": 404, "msg": "训练记录不存在"}
    return {"code": 200, "msg": "校准成功，该样本已加权为高优先级训练数据"}


@train_router.delete("/record/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(AiAutoChat).filter(AiAutoChat.id == record_id).first()
    if not record:
        return {"code": 404, "msg": "训练记录不存在"}
    db.delete(record)
    db.commit()
    return {"code": 200, "msg": "训练记录已删除"}
