#!/bin/bash

# GitHub 部署脚本
# 用于将知识库网站部署到 GitHub Pages

REPO_URL=$1
BRANCH=${2:-gh-pages}

if [ -z "$REPO_URL" ]; then
    echo "用法: $0 <github_repo_url> [branch_name]"
    echo "示例: $0 https://github.com/username/nuclear-kpi-knowledge-base.git gh-pages"
    exit 1
fi

echo "开始部署知识库到 GitHub..."

# 生成最新网站
python3 generate_knowledge_website.py

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo "使用临时目录: $TEMP_DIR"

# 复制网站文件到临时目录
cp -r knowledge_website/* "$TEMP_DIR/"

# 初始化 git 仓库
cd "$TEMP_DIR"
git init
git remote add origin "$REPO_URL"
git checkout -b "$BRANCH"

# 添加所有文件
git add .
git commit -m "Update knowledge base website $(date)"

# 推送到 GitHub
git push -f origin "$BRANCH"

# 清理
cd - > /dev/null
rm -rf "$TEMP_DIR"

echo "知识库网站已部署到 GitHub!"
echo "访问地址: https://<username>.github.io/<repository-name>"