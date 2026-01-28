# GitHub 集成指南

## 设置 GitHub 仓库

1. **创建 GitHub 仓库**：
   - 登录 GitHub 账户
   - 点击 "New repository"
   - 仓库名称建议：`nuclear-kpi-knowledge-base` 或类似名称
   - 选择 Public 或 Private（根据您的隐私需求）
   - 不要初始化 README、.gitignore 或 license（我们会稍后推送内容）

2. **启用 GitHub Pages**：
   - 进入仓库设置
   - 找到 "Pages" 选项
   - 将源设置为 "Deploy from a branch"
   - 选择 "gh-pages" 分支
   - 点击 "Save"

## 部署到 GitHub

### 方法一：使用部署脚本

```bash
# 给脚本执行权限
chmod +x github_deploy.sh

# 部署到 GitHub（替换为您的仓库地址）
./github_deploy.sh https://github.com/<username>/nuclear-kpi-knowledge-base.git
```

### 方法二：手动部署

```bash
# 生成最新网站
python3 generate_knowledge_website.py

# 进入网站目录
cd knowledge_website

# 初始化 git
git init
git remote add origin https://github.com/<username>/nuclear-kpi-knowledge-base.git
git checkout -b gh-pages

# 添加文件并提交
git add .
git commit -m "Initial knowledge base website deployment"

# 推送到 GitHub
git push -f origin gh-pages
```

## 自动化更新

您还可以设置一个脚本来自动更新 GitHub 上的知识库：

```bash
#!/bin/bash
# update_knowledge_base.sh

# 生成最新网站
python3 generate_knowledge_website.py

# 进入网站目录
cd knowledge_website

# 添加所有更改
git add .
git commit -m "Update knowledge base $(date)"

# 推送到 GitHub
git push origin gh-pages

echo "知识库已更新到 GitHub"
```

## 访问您的知识库

部署完成后，您可以通过以下地址访问：
`https://<username>.github.io/<repository-name>`

例如：`https://fan.github.io/nuclear-kpi-knowledge-base`

## 安全注意事项

- 如果使用私有仓库，只有您和您授权的用户可以访问
- 如果使用公共仓库，任何人都可以访问网站内容
- 考虑到核电行业的敏感性，建议使用私有仓库

## 优势

1. **版本控制**：所有更改都有历史记录
2. **备份**：数据在 GitHub 服务器上得到备份
3. **访问便利**：可通过互联网随时访问
4. **协作友好**：可以邀请同事查看或贡献
5. **免费**：GitHub Pages 免费托管静态网站