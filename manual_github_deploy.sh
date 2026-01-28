#!/bin/bash

# 手动部署知识库到 GitHub 的简化脚本

echo "开始手动部署核电考核管理知识库到 GitHub..."

# 生成最新网站
echo "生成最新网站..."
python3 generate_knowledge_website.py

# 检查是否已存在临时仓库
if [ -d "temp_repo" ]; then
    echo "更新现有仓库..."
    cd temp_repo
    git pull origin gh-pages
    cd ..
else
    echo "克隆仓库..."
    git clone https://github.com/Koala-Fan/nuclear-kpi-knowledge-base.git temp_repo
    cd temp_repo
    git checkout -b gh-pages 2>/dev/null || git checkout gh-pages
    cd ..
fi

# 复制网站文件到仓库
echo "复制文件到仓库..."
cp -r knowledge_website/* temp_repo/

# 提交更改
cd temp_repo
git add .
if git diff --cached --quiet; then
    echo "没有更改需要提交"
else
    git config user.name "Knowledge Assistant"
    git config user.email "assistant@example.com"
    git commit -m "Update knowledge base website $(date)"
    echo "文件已提交到本地仓库"
    echo "现在请手动推送更改到 GitHub:"
    echo "1. 配置您的 GitHub 凭据（见 GITHUB_DEPLOYMENT_GUIDE.md）"
    echo "2. 运行: git push origin gh-pages"
fi

cd ..

echo "部署准备完成！请按以下步骤完成部署："
echo ""
echo "如果您已配置 GitHub 凭据："
echo "  cd temp_repo && git push origin gh-pages"
echo ""
echo "如果您尚未配置凭据，请先参考 GITHUB_DEPLOYMENT_GUIDE.md 中的方案进行配置。"
echo ""
echo "部署完成后，您可以通过以下地址访问您的知识库："
echo "  https://Koala-Fan.github.io/nuclear-kpi-knowledge-base/"