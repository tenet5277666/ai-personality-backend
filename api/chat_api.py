from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from core.database import get_db
from core.personality_priority import build_system_prompt
from rag.vector_core import search_rag, insert_rag_sample
from ai_engine.llm_core import call_llm
from db.models import ChatHistory

chat_router = APIRouter()


class ChatSendRequest(BaseModel):
    avatar_id: int
    message: str
    emotion_type: str = "calm"
    social_type: str = "inner"


@chat_router.post("/send")
def chat_send(req: ChatSendRequest, db: Session = Depends(get_db)):
    """核心对话接口"""
    # 1. 保存用户消息
    user_history = ChatHistory(avatar_id=req.avatar_id, role="user", content=req.message,
                               emotion_type=req.emotion_type, social_type=req.social_type)
    db.add(user_history)

    # 2. 构建系统Prompt
    system_prompt = build_system_prompt(db, req.avatar_id, req.emotion_type, req.social_type)

    # 3. 分层RAG检索
    rag_results = search_rag(req.avatar_id, req.message, emotion_type=req.emotion_type,
                             social_type=req.social_type, top_k=5)
    rag_context = "\n".join([f"[参考风格] {content}" for _, content, _ in rag_results]) if rag_results else ""

    # 4. 获取最近聊天历史
    recent_history = db.query(ChatHistory).filter(
        ChatHistory.avatar_id == req.avatar_id
    ).order_by(ChatHistory.create_time.desc()).limit(10).all()
    recent_history.reverse()
    history_text = "\n".join([f"{'用户' if h.role == 'user' else 'AI'}: {h.content}"
                              for h in recent_history])

    # 5. 合成完整Prompt
    full_prompt = f"{system_prompt}\n\n"
    if rag_context:
        full_prompt += f"以下是你可以参考的说话风格素材：\n{rag_context}\n\n"
    if history_text:
        full_prompt += f"以下是最近的聊天记录作为上下文：\n{history_text}\n\n"
    full_prompt += (f"用户刚才说：「{req.message}」\n"
                    "请以第一人称自然回复，不要暴露你是AI，保持人格一致性。"
                    "回复不要太长，像真人微信聊天。回复不要带任何前缀说明。")

    # 6. 调用大模型
    ai_response = call_llm(full_prompt, system_prompt="你是一个有稳定人格的真实人类，"
                           "按照你的人设自然地回复聊天消息。")
    if not ai_response:
        ai_response = "嗯嗯，我收到了！"

    # 7. 保存AI回复
    ai_history = ChatHistory(avatar_id=req.avatar_id, role="ai", content=ai_response,
                              emotion_type=req.emotion_type, social_type=req.social_type)
    db.add(ai_history)
    db.commit()

    # 8. 异步入库RAG
    if len(req.message) > 5:
        insert_rag_sample(user_id=req.avatar_id, avatar_id=req.avatar_id,
                          emotion_type=req.emotion_type, social_type=req.social_type,
                          content=req.message, weight=1)

    return {"code": 200, "data": {"reply": ai_response, "emotion_type": req.emotion_type,
                                   "social_type": req.social_type}}


@chat_router.get("/history")
def chat_history(avatar_id: int, page: int = 1, size: int = 20, db: Session = Depends(get_db)):
    total = db.query(ChatHistory).filter(ChatHistory.avatar_id == avatar_id).count()
    records = db.query(ChatHistory).filter(
        ChatHistory.avatar_id == avatar_id
    ).order_by(ChatHistory.create_time.desc()).offset((page - 1) * size).limit(size).all()
    records.reverse()
    data = [{"id": r.id, "role": r.role, "content": r.content, "emotion_type": r.emotion_type,
             "social_type": r.social_type, "create_time": str(r.create_time)} for r in records]
    return {"code": 200, "data": {"total": total, "page": page, "list": data}}
