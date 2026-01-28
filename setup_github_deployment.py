#!/usr/bin/env python3
"""
GitHub 仓库部署助手
用于引导用户完成 GitHub 仓库设置和部署
"""

import subprocess
import sys
import os
from pathlib import Path


def create_deployment_script(repo_url):
    """创建部署脚本"""
    script_content = f'''#!/bin/bash

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
    git remote add origin {repo_url}
else
    echo "Git 仓库已存在，更新远程地址..."
    git remote set-url origin {repo_url}
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
        echo "https://{repo_url.split("/")[-1].replace(".git", "")}.github.io/"
    else
        echo "部署失败，请检查错误信息"
        exit 1
    fi
fi

echo "部署完成！"
'''
    
    with open('deploy_to_github.sh', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # 设置执行权限
    os.chmod('deploy_to_github.sh', 0o755)
    print("部署脚本已创建: deploy_to_github.sh")


def main():
    print("=== GitHub 仓库部署助手 ===\n")
    
    print("请按以下步骤创建 GitHub 仓库：\n")
    
    print("1. 登录 GitHub: https://github.com")
    print("2. 点击右上角的 '+' 号号，选择 'New repository'")
    print("3. 填写仓库信息：")
    print("   - Repository name: nuclear-kpi-knowledge-base")
    print("   - Description: Nuclear Power Plant KPI Management Knowledge Base")
    print("   - Privacy: Private 或 Public (根据您的需求)")
    print("   - 注意：不要勾选 'Initialize this repository with a README'\n")
    
    print("4. 点击 'Create repository'\n")
    
    print("5. 仓库创建完成后，获取仓库地址：")
    print("   - 点击绿色的 'Code' 按钮")
    print("   - 选择 'HTTPS'")
    print("   - 复制仓库地址（类似：https://github.com/用户名/nuclear-kpi-knowledge-base.git）\n")
    
    print("6. （可选）配置 GitHub Pages：")
    print("   - 在仓库页面点击 'Settings' 标签")
    print("   - 找到左侧的 'Pages' 选项")
    print("   - Source 选择 'Deploy from a branch'")
    print("   - Branch 选择 'gh-pages' 并保持根目录为 '/root'")
    print("   - 点击 'Save'\n")
    
    print("当您准备好仓库地址后，请运行以下命令进行部署：")
    print("python3 setup_github_deployment.py deploy <your_repo_url>")
    
    # 检查参数
    if len(sys.argv) >= 3 and sys.argv[1] == 'deploy':
        repo_url = sys.argv[2]
        print(f"\n正在为仓库 {repo_url} 创建部署脚本...")
        create_deployment_script(repo_url)
        print(f"\n部署脚本已创建完成！")
        print(f"现在您可以运行 './deploy_to_github.sh' 来部署知识库到 GitHub")
    elif len(sys.argv) == 2 and sys.argv[1] == 'deploy':
        print("\n错误: 请提供仓库地址")
        print("用法: python3 setup_github_deployment.py deploy <your_repo_url>")


if __name__ == "__main__":
    main()