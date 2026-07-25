FROM python:3.13-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# 先装依赖（利用 Docker 缓存层）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# 暴露端口
EXPOSE 8100

# 启动命令（Railway/腾讯云会通过环境变量注入 PORT）
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8100}"]
