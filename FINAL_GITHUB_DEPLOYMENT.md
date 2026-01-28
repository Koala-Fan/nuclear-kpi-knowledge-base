# GitHub 部署完成指南

## 当前状态
- 知识库网站已生成并包含所有内容
- Git 仓库已配置正确
- 远程仓库已设置为您的 GitHub 仓库

## 部署选项

### 选项 1：使用 GitHub 网页界面（推荐，避免认证问题）

1. 访问您的 GitHub 仓库：https://github.com/Koala-Fan/nuclear-kpi-knowledge-base
2. 点击 "Add file" > "Upload files"
3. 将 `knowledge_website` 目录中的所有文件拖拽到上传区域：
   - conversations_2026-01-28T08-04-17.266229.html
   - index.html
   - nuclear_kpi_考核指标_反应堆功率调节系统考核要点_2026-01-28_14-00-31.html
   - nuclear_performance_核电人员考核_核电站运行人员绩效考核要点_2026-01-28_14-03-01.html
   - nuclear_performance_核电技术体系_反应堆功率调节系统概述_2026-01-28_14-02-58.html
   - research_2026-01-28T08-14-47.670440.html
   - research_2026-01-28T08-14-51.926223.html
4. 提交更改时，切换到 `gh-pages` 分支：
   - 在提交消息下方，找到 "Commit directly to the `main` branch." 
   - 点击下拉菜单，选择 "Create a new branch for this commit and start a pull request."
   - 将分支名称改为 `gh-pages`
   - 点击 "Propose changes"
5. 在 Pull Request 页面，点击 "Merge pull request"，然后 "Confirm merge"
6. 或者，您也可以直接在上传时切换到 gh-pages 分支（如果可用）

### 选项 2：使用 GitHub Desktop
1. 下载并安装 GitHub Desktop
2. 克隆您的仓库
3. 将 `knowledge_website` 目录中的文件复制到本地仓库
4. 提交并推送到 `gh-pages` 分支

### 选项 3：配置认证后使用命令行
按照 GITHUB_AUTH_SETUP.md 中的说明配置认证，然后运行：
```bash
cd knowledge_website
git add .
git config user.name "Knowledge Assistant"
git config user.email "assistant@example.com"
git commit -m "Update knowledge base website"
git push origin gh-pages
```

## 配置 GitHub Pages

1. 在仓库页面，点击 "Settings" 选项卡
2. 找到左侧的 "Pages" 选项
3. Source 选择 "Deploy from a branch"
4. Branch 选择 "gh-pages" 并保持根目录为 "/root"
5. 点击 "Save"

## 访问您的知识库

配置完成后，您可以通过以下地址访问：
https://Koala-Fan.github.io/nuclear-kpi-knowledge-base/

## 后续更新

当您添加新知识并重新生成网站后（运行 `python3 generate_knowledge_website.py`），重复上述上传步骤即可更新在线知识库。

您的核电与考核管理知识库现已准备就绪，只需完成最后的部署步骤即可在线访问！