#!/bin/bash
# ============================================
# AI专属人设训练APP - 一键部署脚本
# 在腾讯云轻量服务器上执行
# ============================================
set -e

echo "=========================================="
echo "  AI专属人设训练APP - 部署脚本"
echo "=========================================="

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "[1/5] 安装 Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
else
    echo "[1/5] Docker 已安装"
fi

# 检查 docker-compose
if ! docker compose version &> /dev/null 2>&1; then
    echo "  安装 docker-compose 插件..."
    apt-get update -qq && apt-get install -y -qq docker-compose-plugin
fi

# 检查 .env 文件
if [ ! -f .env ]; then
    echo "[2/5] 创建 .env 文件..."
    cp .env.production .env
    echo ""
    echo "  ⚠️  请编辑 .env 文件，修改 DB_PASSWORD 和 SECRET_KEY"
    echo "  命令: nano .env"
    echo "  修改后重新运行: ./deploy.sh"
    exit 1
fi

echo "[2/5] .env 配置已存在"

# 构建并启动
echo "[3/5] 构建 Docker 镜像..."
docker compose build --no-cache

echo "[4/5] 启动服务..."
docker compose up -d

echo "[5/5] 等待服务就绪..."
sleep 10

# 健康检查
for i in $(seq 1 10); do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost/api/avatar/list | grep -q "200\|422"; then
        echo ""
        echo "=========================================="
        echo "  ✅ 部署成功！"
        echo "=========================================="
        echo ""
        echo "  前端: http://$(curl -s ifconfig.me)/"
        echo "  API:  http://$(curl -s ifconfig.me)/api/"
        echo "  文档: http://$(curl -s ifconfig.me)/docs"
        echo ""
        echo "  备案通过后，在 nginx.conf 中配置域名和 SSL"
        echo "=========================================="
        exit 0
    fi
    echo -n "."
    sleep 3
done

echo ""
echo "❌ 部署可能失败，检查日志："
echo "  docker compose logs"
exit 1
