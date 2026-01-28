#!/bin/bash

# 自动部署知识库到 GitHub
# 请在运行前确保您已安装 git 并配置了 GitHub 访问权限

echo "开始部署核电考核管理知识库到 GitHub..."

# 生成最新网站
python3 generate_knowledge_website.py

# 进入网站目录
cd knowledge_website

# 检查是否已有 git 仓库
if [ ! -d ".git" ]; then
    echo "初始化 Git 仓库..."
    git init
    git checkout -b gh-pages
    git remote add origin https://github.com/Koala-Fan/nuclear-kpi-knowledge-base.git
else
    echo "Git 仓库已存在，更新远程地址..."
    git remote set-url origin https://github.com/Koala-Fan/nuclear-kpi-knowledge-base.git
fi

# 添加所有文件
git add .

# 检查是否有更改
if git diff-index --quiet HEAD --; then
    echo "没有更改需要提交"
else
    # 提交更改
    git config user.name "Knowledge Assistant"
    git config user.email "assistant@example.com"
    git commit -m "Update knowledge base website $(date '+%Y-%m-%d %H:%M:%S')"
    
    # 推送到 GitHub
    echo "推送到 GitHub..."
    git push -f origin gh-pages
    
    if [ $? -eq 0 ]; then
        echo "成功部署到 GitHub!"
        echo "您的知识库可以通过以下地址访问:"
        echo "https://nuclear-kpi-knowledge-base.github.io/"
    else
        echo "部署失败，请检查错误信息"
        exit 1
    fi
fi

echo "部署完成！"
