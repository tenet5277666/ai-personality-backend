from sqlalchemy.orm import Session
from db.models import PersonalityBase, PersonalityWVW, PersonalityEmotion, SocialTrain


def build_system_prompt(db: Session, avatar_id: int, emotion_type: str = "calm", social_type: str = "inner") -> str:
    """
    动态合成AI人格Prompt，按优先级：三观 > 基础人设 > 情绪体系 > 社交风格
    """
    parts = []

    # 1. 三观伦理库 (最高优先)
    wvw = db.query(PersonalityWVW).filter(PersonalityWVW.avatar_id == avatar_id).first()
    if wvw:
        parts.append("【三观内核】")
        parts.append(f"- 世界观：{wvw.world_view}")
        parts.append(f"- 人生观：{wvw.life_view}")
        parts.append(f"- 价值观：{wvw.value_view}")
        parts.append("以上三观是你回答一切问题的底层逻辑和思想准则，不可违背。\n")

    # 2. 基础人设
    base = db.query(PersonalityBase).filter(PersonalityBase.avatar_id == avatar_id).first()
    if base:
        parts.append("【基础人设】")
        if base.age:
            parts.append(f"- 年龄：{base.age}")
        if base.identity:
            parts.append(f"- 身份：{base.identity}")
        parts.append(f"- 语速风格：{base.talk_speed}")
        if base.hobby:
            parts.append(f"- 爱好：{base.hobby}")
        if base.taboo:
            parts.append(f"- 禁忌（绝不能说）：{base.taboo}")
        if base.advantage:
            parts.append(f"- 优点：{base.advantage}")
        if base.disadvantage:
            parts.append(f"- 缺点：{base.disadvantage}")
        parts.append("")

    # 3. 当前情绪体系
    emotion_record = db.query(PersonalityEmotion).filter(
        PersonalityEmotion.avatar_id == avatar_id,
        PersonalityEmotion.emotion_type == emotion_type
    ).first()
    if emotion_record:
        parts.append(f"【当前情绪：{emotion_type}】")
        if emotion_record.trigger_rule:
            parts.append(f"- 触发条件：{emotion_record.trigger_rule}")
        if emotion_record.feature:
            parts.append(f"- 情绪特征：{emotion_record.feature}")
        parts.append(f"- 情绪强度：{emotion_record.intensity}/10")
        parts.append("")

    # 4. 社交风格
    social_record = db.query(SocialTrain).filter(
        SocialTrain.avatar_id == avatar_id,
        SocialTrain.social_type == social_type
    ).first()
    if social_record and social_record.social_feature:
        social_label = "对内私密风格" if social_type == "inner" else "对外社交风格"
        parts.append(f"【{social_label}】")
        parts.append(f"{social_record.social_feature}")
        parts.append("")

    if not parts:
        return "你是一个自然、真实、有温度的AI助手，像真人朋友一样聊天。"

    system_prompt = "\n".join(parts)
    return system_prompt
