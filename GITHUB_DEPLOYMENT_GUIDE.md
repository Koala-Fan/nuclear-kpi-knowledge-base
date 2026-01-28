# GitHub 部署指南

## 问题诊断
部署失败是因为 Git 无法获取您的 GitHub 用户名和密码。以下是几种解决方案：

## 方案一：使用 Personal Access Token（推荐）

### 1. 创建 Personal Access Token
1. 登录 GitHub
2. 点击头像，选择 "Settings"
3. 在左侧菜单中选择 "Developer settings"
4. 选择 "Personal access tokens" > "Tokens (classic)"
5. 点击 "Generate new token"
6. 选择 "repo" 权限
7. 复制生成的 token

### 2. 配置 Git 使用 token
```bash
# 将 <token> 替换为您复制的 token
git config --global credential.helper store
git clone https://<token>@github.com/Koala-Fan/nuclear-kpi-knowledge-base.git
```

## 方案二：使用 SSH（推荐用于长期使用）

### 1. 生成 SSH 密钥
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 2. 添加 SSH 密钥到 GitHub
1. 复制公钥内容：
```bash
cat ~/.ssh/id_ed25519.pub
```
2. 在 GitHub 中添加 SSH 密钥：
   - Settings > SSH and GPG keys
   - 点击 "New SSH key"
   - 粘贴公钥内容

### 3. 修改仓库 URL
```bash
# 将仓库 URL 从 HTTPS 改为 SSH
git remote set-url origin git@github.com:Koala-Fan/nuclear-kpi-knowledge-base.git
```

## 方案三：临时解决方案
您可以手动部署一次：

```bash
# 1. 生成最新网站
python3 generate_knowledge_website.py

# 2. 手动克隆仓库
git clone https://github.com/Koala-Fan/nuclear-kpi-knowledge-base.git temp_repo
cd temp_repo

# 3. 复制网站文件
cp -r ../knowledge_website/* .

# 4. 提交更改
git checkout -b gh-pages
git add .
git config user.name "Knowledge Assistant"
git config user.email "assistant@example.com"
git commit -m "Update knowledge base website $(date)"
git push origin gh-pages
```

## 后续更新
一旦配置好认证，您可以使用以下命令更新知识库：

```bash
# 生成新内容
python3 generate_knowledge_website.py

# 进入仓库目录
cd temp_repo

# 复制新文件
cp -r ../knowledge_website/* .

# 提交更改
git add .
git commit -m "Update knowledge base $(date)"
git push origin gh-pages
```

## 访问您的网站
部署完成后，您可以通过以下地址访问：
https://Koala-Fan.github.io/nuclear-kpi-knowledge-base/

注意：首次部署可能需要几分钟才能生效。