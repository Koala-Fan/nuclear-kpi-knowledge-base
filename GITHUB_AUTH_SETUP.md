# GitHub 认证配置指南

## 方法一：使用 GitHub CLI（推荐）

### 1. 安装 GitHub CLI
```bash
# Mac
brew install gh

# 或者从官网下载
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 2. 登录 GitHub
```bash
gh auth login
```
- 选择 "HTTPS"
- 选择 "Login with a web browser"
- 按照提示完成认证

### 3. 配置 Git 凭据助手
```bash
gh auth setup-git
```

## 方法二：使用 Personal Access Token

### 1. 创建 Personal Access Token
- 登录 GitHub
- 访问 Settings > Developer settings > Personal access tokens > Tokens (classic)
- 点击 "Generate new token"
- 选择 "repo" 权限
- 复制生成的 token

### 2. 配置 Git 存储凭证
```bash
git config --global credential.helper store
```

### 3. 第一次推送时使用 token
```bash
git clone https://github.com/Koala-Fan/nuclear-kpi-knowledge-base.git
# 或者在已有的仓库中：
git remote set-url origin https://<token>@github.com/Koala-Fan/nuclear-kpi-knowledge-base.git
```

## 完成部署

配置好认证后，运行以下命令完成部署：

```bash
# 1. 进入临时仓库
cd temp_repo

# 2. 设置正确的分支
git checkout -b gh-pages

# 3. 提交更改
git add .
git config user.name "Knowledge Assistant"
git config user.email "assistant@example.com"
git commit -m "Initial knowledge base website deployment"

# 4. 推送到 GitHub
git push -u origin gh-pages
```

## 验证部署

部署完成后：
1. 访问 GitHub 仓库页面
2. 确认 gh-pages 分支已创建
3. 在 Settings > Pages 中确认源为 gh-pages 分支

## 访问网站

部署成功后，您可以通过以下地址访问知识库：
https://Koala-Fan.github.io/nuclear-kpi-knowledge-base/

注意：首次部署可能需要几分钟到几小时生效，具体取决于 GitHub Pages 的处理速度。