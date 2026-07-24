from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from core.database import Base


# 用户表
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone = Column(String(20), unique=True, nullable=False)
    avatar = Column(String(255), default="")
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())


# AI分身表
class UserAvatar(Base):
    __tablename__ = "user_avatar"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    avatar_name = Column(String(50), default="我的AI分身")
    train_type = Column(String(30), nullable=False)
    birthday = Column(String(20), default="")
    constellation = Column(String(20), default="")
    status = Column(Integer, default=1)
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())


# 基础人设表
class PersonalityBase(Base):
    __tablename__ = "personality_base"
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar_id = Column(Integer, nullable=False, unique=True)
    age = Column(String(20), default="")
    identity = Column(String(50), default="")
    talk_speed = Column(String(20), default="normal")
    hobby = Column(Text, default="")
    taboo = Column(Text, default="")
    advantage = Column(Text, default="")
    disadvantage = Column(Text, default="")
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())


# 三观伦理库
class PersonalityWVW(Base):
    __tablename__ = "personality_wvw"
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar_id = Column(Integer, nullable=False)
    is_init_constellation = Column(Integer, default=0)
    world_view = Column(Text, default="")
    life_view = Column(Text, default="")
    value_view = Column(Text, default="")
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())


# 情绪训练表
class PersonalityEmotion(Base):
    __tablename__ = "personality_emotion"
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar_id = Column(Integer, nullable=False)
    emotion_type = Column(String(20), nullable=False)
    trigger_rule = Column(Text, default="")
    feature = Column(Text, default="")
    intensity = Column(Integer, default=5)
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())


# 情绪样本表
class EmotionSample(Base):
    __tablename__ = "emotion_sample"
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar_id = Column(Integer, nullable=False)
    emotion_type = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    create_time = Column(DateTime, default=func.now())


# 社交训练表
class SocialTrain(Base):
    __tablename__ = "social_train"
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar_id = Column(Integer, nullable=False)
    social_type = Column(String(20), nullable=False)
    social_feature = Column(Text, default="")
    create_time = Column(DateTime, default=func.now())
    update_time = Column(DateTime, default=func.now(), onupdate=func.now())


# AI自主训练记录表
class AiAutoChat(Base):
    __tablename__ = "ai_auto_chat"
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar_id = Column(Integer, nullable=False)
    emotion_type = Column(String(20), default="")
    social_type = Column(String(20), default="")
    ai_content = Column(Text, nullable=False)
    user_correct_content = Column(Text, default="")
    is_correct = Column(Integer, default=0)
    weight = Column(Integer, default=1)
    create_time = Column(DateTime, default=func.now())


# 聊天记录表
class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    avatar_id = Column(Integer, nullable=False)
    role = Column(String(10), nullable=False)
    content = Column(Text, nullable=False)
    emotion_type = Column(String(20), default="")
    social_type = Column(String(20), default="")
    create_time = Column(DateTime, default=func.now())
