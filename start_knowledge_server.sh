#!/bin/bash
# 启动核电考核管理知识库本地服务器

echo "==========================================="
echo "核电考核管理知识库本地服务器"
echo "==========================================="
echo "启动时间: $(date)"
echo "访问地址: http://localhost:8000"
echo "按 Ctrl+C 停止服务器"
echo "==========================================="

# 生成最新网站
echo "正在生成最新网站内容..."
python3 generate_knowledge_website.py

echo "网站已更新，启动本地服务器..."

# 进入网站目录并启动服务器
cd knowledge_website
python3 -m http.server 8000