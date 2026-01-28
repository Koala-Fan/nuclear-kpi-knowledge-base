# Notion 知识库系统

## 概述

这是一个完整的知识管理系统，可以将对话、研究和AI生成的内容自动保存到您的 Notion 空间中。系统支持分类、标签和检索功能。

## 设置步骤

### 1. 创建 Notion Integration
- 访问 [Notion Integrations 页面](https://www.notion.so/my-integrations)
- 点击 "New integration"
- 输入名称（例如：Knowledge Base Assistant）
- 选择您的 Notion 工作区
- 记下生成的 "Internal Integration Token"

### 2. 设置环境变量
```bash
export NOTION_TOKEN='your_integration_token_here'
```

### 3. 在 Notion 中创建知识库页面
- 在您的 Notion 工作区中创建一个新的页面，命名为 "Knowledge Base"
- 记下此页面的 ID（从 URL 中获取）

### 4. 共享页面给集成
- 在知识库页面上，点击右上角的 "Share" 按钮
- 搜索并添加您刚创建的集成
- 授予 "Read and write" 权限

### 5. 创建知识库数据库
```bash
python3 notion_knowledge_helper.py create_db <your_parent_page_id>
```

## 使用方法

### 添加知识条目
```bash
# 基本用法
python3 notion_knowledge_helper.py add <database_id> "知识内容" "类型" "标签1,标签2"

# 示例
python3 notion_knowledge_helper.py add abc123 "今天学习了Notion API的使用方法" "Research" "notion,api,learning" "Notion API 学习笔记"
```

### 类型说明
- `Conversation` - 对话记录
- `Research` - 研究资料
- `Generated` - AI 生成内容
- `Report` - 报告材料

## 与 AI 助手集成

您可以请求助手将信息保存到知识库：

> "请将以上信息保存到知识库，类型为 Research，标签为 ai,ml"

助手将使用上述命令将信息保存到您的 Notion 知识库中。

## 优势

1. **跨平台访问** - Notion 有优秀的网页版和移动应用
2. **同步可靠** - Notion 的同步机制比 iCloud 更稳定
3. **功能丰富** - 支持数据库、表格、标签等多种组织方式
4. **协作友好** - 可以轻松分享给他人
5. **搜索强大** - Notion 内置强大的搜索功能

## 故障排除

如果遇到问题：
1. 确认 NOTION_TOKEN 已正确设置
2. 确认集成已添加到知识库页面
3. 检查集成是否有适当的读写权限