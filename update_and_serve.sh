#!/bin/bash

# 更新知识库网站并启动本地服务器

echo "正在更新知识库网站..."
python3 generate_knowledge_website.py

echo "网站已更新，正在启动本地服务器..."

# 启动服务器在后台
python3 deploy_knowledge_website.py serve &
SERVER_PID=$!

echo "知识库网站已在 http://localhost:8000 启动"
echo "PID: $SERVER_PID"
echo "按 Ctrl+C 停止服务器"

# 等待服务器进程
wait $SERVER_PID