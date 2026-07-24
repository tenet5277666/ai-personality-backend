"""
Simple in-memory IP rate limiter.
No external dependencies. Sliding 60-second window per IP.
"""
import time
from collections import defaultdict
from fastapi import Request
from fastapi.responses import JSONResponse


class RateLimiter:
    def __init__(self, limit: int = 60, window: int = 60):
        self.limit = limit
        self.window = window          # seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    def _clean(self, ip: str):
        now = time.time()
        cutoff = now - self.window
        self._hits[ip] = [t for t in self._hits[ip] if t > cutoff]

    def check(self, ip: str) -> bool:
        self._clean(ip)
        if len(self._hits[ip]) >= self.limit:
            return False
        self._hits[ip].append(time.time())
        return True


# Per-endpoint limits (each IP has its own window per path)
# 上线额度：对话 30次/分，训练 15次/分，通用 120次/分
_CHAT_LIMITER = RateLimiter(limit=30, window=60)     # /api/chat/send
_TRAIN_LIMITER = RateLimiter(limit=15, window=60)    # /api/train/auto
_GENERAL_LIMITER = RateLimiter(limit=120, window=60)  # everything else

_EXPENSIVE_PREFIXES = {
    "/api/chat/send": _CHAT_LIMITER,
    "/api/train/auto": _TRAIN_LIMITER,
}


async def rate_limit_middleware(request: Request, call_next):
    # Only limit API routes
    if not request.url.path.startswith("/api/"):
        return await call_next(request)

    client_ip = request.client.host if request.client else "unknown"

    for prefix, limiter in _EXPENSIVE_PREFIXES.items():
        if request.url.path == prefix:
            if not limiter.check(client_ip):
                return JSONResponse(status_code=429, content={"detail": "请求过于频繁，请稍后再试"})
            return await call_next(request)

    # General fallback
    if not _GENERAL_LIMITER.check(client_ip):
        return JSONResponse(status_code=429, content={"detail": "请求过于频繁，请稍后再试"})

    return await call_next(request)
