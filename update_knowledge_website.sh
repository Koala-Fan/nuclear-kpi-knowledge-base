#!/bin/bash
# 更新知识库网站并同步到iCloud

echo "正在更新知识库网站..."

# 生成最新网站
python3 generate_knowledge_website.py

# 同步到iCloud
echo "正在同步到iCloud..."
cp -r knowledge_website ~/Library/Mobile\ Documents/com~apple~CloudDocs/

echo "知识库网站已更新并同步到iCloud，可在iOS设备上通过Safari访问。"