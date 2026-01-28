#!/bin/bash

# 验证仓库是否存在并部署知识库

TOKEN="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"
USERNAME="Koala-Fan"
REPO_NAME="nuclear-kpi-knowledge-base"

echo "正在验证仓库 $USERNAME/$REPO_NAME 是否存在..."

# 检查仓库是否存在
if curl -s -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/$USERNAME/$REPO_NAME" | grep -q "name"; then
  
  echo "仓库存在，正在部署知识库..."
  
  # 进入知识库目录
  cd knowledge_website
  
  # 确保远程 URL 包含 token
  git remote set-url origin "https://${TOKEN}@github.com/${USERNAME}/${REPO_NAME}.git"
  
  # 推送到 gh-pages 分支
  echo "推送知识库到 GitHub..."
  git push origin gh-pages
  
  if [ $? -eq 0 ]; then
    echo "成功部署到 GitHub!"
    echo "访问地址: https://${USERNAME}.github.io/${REPO_NAME}/"
  else
    echo "推送失败，可能需要先初始化仓库"
    echo "尝试推送 master 分支..."
    
    # 如果 gh-pages 不存在，先推送到默认分支
    git push origin main || git push origin master
    
    # 然后创建并切换到 gh-pages 分支
    git checkout -b gh-pages
    git push -u origin gh-pages
  fi
else
  echo "仓库不存在或访问被拒绝"
  echo "请确认:"
  echo "1. 仓库已创建"
  echo "2. 您有写入权限"
  echo "3. Token 有正确的权限"
fi