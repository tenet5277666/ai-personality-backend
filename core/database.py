from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.settings import DATABASE_URL, USE_SQLITE, DB_TYPE
import os

if USE_SQLITE:
    # SQLite：零配置本地模式
    DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ai_personality_v2.db")
    DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    pool_size=10 if not USE_SQLITE else 1,
    max_overflow=20,
    echo=False,
    pool_pre_ping=True if not USE_SQLITE else False,
    connect_args={"check_same_thread": False} if USE_SQLITE else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI 依赖注入"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()