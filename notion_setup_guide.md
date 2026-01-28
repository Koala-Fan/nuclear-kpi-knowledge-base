# Notion 知识库设置指南

## 第一步：创建 Notion Integration

1. 访问 [Notion Integrations 页面](https://www.notion.so/my-integrations)
2. 点击 "New integration"
3. 输入名称（例如：Knowledge Base Assistant）
4. 选择您的 Notion 工作区
5. 记下生成的 "Internal Integration Token"

## 第二步：在 Notion 中创建知识库页面

1. 在您的 Notion 工作区中创建一个新的页面，命名为 "Knowledge Base"
2. 这将作为您的知识库主页面

## 第三步：共享页面给集成

1. 在知识库页面上，点击右上角的 "Share" 按钮
2. 搜索并添加您刚创建的集成
3. 授予 "Read and write" 权限

## 第四步：获取页面ID

1. 打开您的知识库页面
2. 复制 URL 中的页面 ID（URL 末尾的长字符串）

## 第五步：设置环境变量

在终端中运行以下命令（替换为您的实际令牌）：

```bash
export NOTION_TOKEN='your_integration_token_here'
```

## 第六步：测试集成

运行以下命令来测试连接：

```bash
python3 notion_knowledge_base.py test
```

## 使用示例

一旦设置完成，您可以使用以下命令向知识库添加条目：

```bash
# 创建知识库数据库
python3 notion_knowledge_helper.py create_db <parent_page_id>

# 添加条目
python3 notion_knowledge_helper.py add <database_id> "内容" "类型" "标签1,标签2"
```