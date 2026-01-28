# 静态网站知识库系统

## 概述

这是一个基于静态网站的个人知识库系统，可以轻松在电脑和手机上访问。系统会自动生成美观的网页，展示您的知识条目。

## 功能特点

- 响应式设计，适配手机和电脑屏幕
- 自动分类和索引知识条目
- 简洁美观的界面
- 无需复杂设置，易于部署

## 使用方法

### 1. 添加新知识条目

使用以下命令将信息添加到知识库：

```bash
# 添加对话类知识
python3 knowledge_base/knowledge_manager.py save "具体内容" "conversation" "标签1,标签2"

# 添加研究类知识
python3 knowledge_base/knowledge_manager.py save "具体内容" "research" "标签1,标签2"

# 添加AI生成类知识
python3 knowledge_base/knowledge_manager.py save "具体内容" "generated" "标签1,标签2"
```

### 2. 更新网站

每当添加新内容后，重新生成网站：

```bash
python3 generate_knowledge_website.py
```

### 3. 本地预览

启动本地服务器预览网站：

```bash
# 启动服务器
python3 deploy_knowledge_website.py serve

# 或者只在浏览器中打开（需先启动服务器）
python3 deploy_knowledge_website.py open

# 重新生成网站
python3 deploy_knowledge_website.py generate
```

### 4. 部署到服务器

将 `knowledge_website` 目录中的所有文件上传到任何支持静态网站托管的服务：

- GitHub Pages
- Netlify
- Vercel
- 任何支持静态文件托管的服务器

## 在手机上访问

### 方法一：本地访问
1. 在电脑上启动本地服务器：`python3 deploy_knowledge_website.py serve`
2. 在手机上使用浏览器访问电脑的IP地址和端口（如 `http://192.168.1.x:8000`）

### 方法二：在线访问
1. 将网站部署到在线托管服务
2. 在手机上直接访问网址

## 日常使用流程

1. 当您想保存有价值的信息时，使用知识管理器保存
2. 定期运行 `generate_knowledge_website.py` 更新网站
3. 通过浏览器访问网站查看和检索知识

## 优势

- 无需担心云同步问题
- 访问速度快
- 完全控制您的数据
- 跨平台兼容
- 适合离线访问（本地部署时）

## 注意事项

- 每次添加新内容后需要重新生成网站
- 本地服务器只在运行时可访问
- 如果要多人访问或持续访问，建议部署到在线服务