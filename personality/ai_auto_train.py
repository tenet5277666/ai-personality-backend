import random
from sqlalchemy.orm import Session
from db.models import AiAutoChat
from rag.vector_core import insert_rag_sample

# 全自动社交场景池
SOCIAL_SCENES = [
    "日常朋友轻松闲聊",
    "普通熟人礼貌寒暄",
    "职场工作沟通对接",
    "陌生人初次认识交流",
    "被人搭话时的回应",
    "委婉拒绝他人请求",
    "安慰情绪低落的人",
    "分享日常心情与状态",
    "轻微争执后的沟通",
    "主动开启话题拉近关系"
]


def auto_gen_social_talk(emotion_type="calm"):
    """根据人设自动生成话题"""
    scene = random.choice(SOCIAL_SCENES)
    prompt = f"你现在需要模拟真实人类，在【{scene}】场景下主动发起一句自然的聊天开场白，情绪状态：{emotion_type}，不要机器感，极度生活化。"
    return scene, prompt


def save_auto_train_record(db: Session, avatar_id, emotion_type, social_type, ai_content):
    """保存AI自动训练对话"""
    new_record = AiAutoChat(
        avatar_id=avatar_id,
        emotion_type=emotion_type,
        social_type=social_type,
        ai_content=ai_content,
        user_correct_content="",
        is_correct=0,
        weight=1
    )
    db.add(new_record)
    db.commit()
    return new_record


def correct_train_record(db: Session, record_id, user_content):
    """用户校准后加权更新"""
    record = db.query(AiAutoChat).filter(AiAutoChat.id == record_id).first()
    if not record:
        return False
    record.user_correct_content = user_content
    record.is_correct = 1
    record.weight = 5
    db.commit()
    insert_rag_sample(
        user_id=record.avatar_id,
        avatar_id=record.avatar_id,
        emotion_type=record.emotion_type,
        social_type=record.social_type,
        content=user_content,
        weight=5
    )
    return True
