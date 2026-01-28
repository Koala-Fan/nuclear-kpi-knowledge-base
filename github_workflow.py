#!/usr/bin/env python3
"""
GitHub 集成工作流程
用于自动化部署知识库到 GitHub Pages
"""

import os
import subprocess
import sys
from pathlib import Path
import argparse


def initialize_git_repo(repo_url, branch='gh-pages'):
    """初始化 git 仓库并连接到远程仓库"""
    print(f"初始化 Git 仓库并连接到 {repo_url}")
    
    # 初始化仓库
    subprocess.run(['git', 'init'], check=True, capture_output=True)
    subprocess.run(['git', 'checkout', '-b', branch], check=True, capture_output=True)
    
    # 添加远程仓库
    subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True, capture_output=True)
    
    print("Git 仓库初始化完成")


def commit_and_push(branch='gh-pages'):
    """提交更改并推送到 GitHub"""
    print(f"提交更改到 {branch} 分支")
    
    # 添加所有更改
    subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
    
    # 提交
    commit_msg = f"Update knowledge base website {subprocess.check_output(['date']).decode().strip()}"
    subprocess.run(['git', 'commit', '-m', commit_msg], 
                   check=False, capture_output=True)  # 使用 check=False 因为可能没有更改
    
    # 推送到远程仓库
    result = subprocess.run(['git', 'push', '-f', 'origin', branch], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print("成功推送到 GitHub")
    else:
        print(f"推送失败: {result.stderr}")


def deploy_to_github(repo_url, branch='gh-pages'):
    """部署知识库到 GitHub"""
    # 生成最新网站
    print("生成最新知识库网站...")
    subprocess.run([sys.executable, 'generate_knowledge_website.py'], check=True)
    
    # 进入网站目录
    original_dir = os.getcwd()
    os.chdir('knowledge_website')
    
    try:
        # 检查是否已经是 git 仓库
        if not Path('.git').exists():
            initialize_git_repo(repo_url, branch)
        
        # 提交并推送
        commit_and_push(branch)
        
        print(f"\n成功部署到 GitHub!")
        print(f"访问地址: https://{repo_url.split('/')[-1].replace('.git', '')}.github.io/")
        
    finally:
        os.chdir(original_dir)


def setup_github_pages():
    """提供 GitHub Pages 设置说明"""
    print("""
GitHub Pages 设置步骤:

1. 创建 GitHub 仓库:
   - 访问 https://github.com/new
   - 输入仓库名称 (如: nuclear-kpi-knowledge-base)
   - 选择 Public 或 Private
   - 不要勾选 "Initialize this repository with a README"

2. 在仓库中启用 GitHub Pages:
   - 进入仓库设置
   - 找到 "Pages" 侧边栏
   - 源(Source)选择 "Deploy from a branch"
   - 分支(Branch)选择 "gh-pages" 并保持根目录(/root)
   - 点击 "Save"

3. 获取仓库地址:
   - 点击 "Code" 按钮
   - 复制 HTTPS 地址 (如: https://github.com/username/repository.git)
    """)


def main():
    parser = argparse.ArgumentParser(description='GitHub 集成工作流程')
    parser.add_argument('action', choices=['setup', 'deploy', 'info'], 
                       help='动作: setup(设置说明), deploy(部署), info(信息)')
    parser.add_argument('--repo-url', help='GitHub 仓库地址')
    parser.add_argument('--branch', default='gh-pages', help='分支名称 (默认: gh-pages)')
    
    args = parser.parse_args()
    
    if args.action == 'setup':
        setup_github_pages()
    elif args.action == 'deploy':
        if not args.repo_url:
            print("错误: 部署需要 --repo-url 参数")
            print("用法: python github_workflow.py deploy --repo-url <github_repo_url>")
            return
        deploy_to_github(args.repo_url, args.branch)
    elif args.action == 'info':
        print("GitHub 集成信息:")
        print("- 使用 gh-pages 分支托管静态网站")
        print("- 通过 GitHub Pages 提供访问")
        print("- 支持自定义域名配置")


if __name__ == "__main__":
    main()