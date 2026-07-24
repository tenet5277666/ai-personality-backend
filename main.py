from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import traceback

from api.user_api import user_router
from api.avatar_api import avatar_router
from api.personality_api import personality_router
from api.chat_api import chat_router
from api.train_api import train_router
from api.admin_api import admin_router

from rag.vector_core import init_vector_store
from core.database import engine, Base
from core.settings import DB_TYPE, VECTOR_DB_PATH, PORT
from core.rate_limit import rate_limit_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用启动/关闭生命周期"""
    # 启动时：建表、初始化向量库
    Base.metadata.create_all(bind=engine)
    init_vector_store()
    print("=" * 50)
    print("AI专属人设训练APP - 后端服务已启动")
    print(f"数据库: {DB_TYPE}")
    print(f"向量存储: 本地文件 -> {VECTOR_DB_PATH}")
    print(f"监听端口: {PORT}")
    print("=" * 50)
    yield
    print("服务关闭中...")


app = FastAPI(
    title="AI专属人设训练APP",
    description="千人千面AI人设分身训练系统",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 限流中间件（优先执行，在异常捕获之前）
app.middleware("http")(rate_limit_middleware)

# 调试中间件：打印500错误（不拦截HTTPException）
@app.middleware("http")
async def debug_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException:
        raise
    except Exception as e:
        print(f"[500 ERROR] {request.method} {request.url.path}: {type(e).__name__}: {e}")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": f"{type(e).__name__}: {str(e)}"}
        )

# 注册路由
app.include_router(user_router, prefix="/api/user", tags=["用户模块"])
app.include_router(avatar_router, prefix="/api/avatar", tags=["分身模块"])
app.include_router(personality_router, prefix="/api/personality", tags=["人设训练模块"])
app.include_router(chat_router, prefix="/api/chat", tags=["对话模块"])
app.include_router(train_router, prefix="/api/train", tags=["AI训练模块"])
app.include_router(admin_router, prefix="/api/admin", tags=["【后台专属】数据投喂与修改"])


@app.get("/")
def root():
    return {"name": "AI专属人设训练APP", "version": "1.0.0", "status": "running"}
