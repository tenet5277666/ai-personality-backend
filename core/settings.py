import os
from pathlib import Path

# 加载 .env 文件（本地开发用；Railway 上用平台环境变量）
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass

# ===== 数据库配置 =====
# 优先级：DATABASE_URL > USE_SQLITE > MySQL 单独配置
# Railway 添加 PostgreSQL 插件后会自动注入 DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", "")

if DATABASE_URL:
    # PostgreSQL 模式（Railway / 任意 PostgreSQL 服务）
    # Railway 提供的 URL 格式: postgresql://user:pass@host:port/dbname
    # SQLAlchemy 需要 postgresql+psycopg2:// 前缀
    if DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
    elif DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    USE_SQLITE = False
    DB_TYPE = "PostgreSQL"
elif os.getenv("USE_SQLITE", "1") == "1":
    USE_SQLITE = True
    DB_TYPE = "SQLite"
else:
    # MySQL 模式
    USE_SQLITE = False
    DB_TYPE = "MySQL"
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASS = os.getenv("DB_PASS", "your_password_here")
    DB_NAME = os.getenv("DB_NAME", "ai_personality")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# 兼容旧代码引用 DB_HOST 等
if not DATABASE_URL and not USE_SQLITE:
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASS = os.getenv("DB_PASS", "your_password_here")
    DB_NAME = os.getenv("DB_NAME", "ai_personality")
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

# ===== 向量库配置（本地文件存储，Railay 上用 /tmp）=====
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", str(Path(__file__).resolve().parent.parent / "chroma_db"))

# ===== 大模型 API 配置 =====
LLM_API_URL = os.getenv("LLM_API_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY")          # 必须通过环境变量设置，无后备值
LLM_MODEL = os.getenv("LLM_MODEL", "qwen-plus")

# ===== JWT 配置 =====
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7天

# ===== 服务端口（Railway 会注入 PORT）=====
PORT = int(os.getenv("PORT", "8100"))