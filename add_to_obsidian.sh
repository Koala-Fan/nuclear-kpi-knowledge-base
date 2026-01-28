#!/bin/bash

# 向现有 Obsidian 仓库添加知识条目的便捷脚本

if [ $# -lt 2 ]; then
    echo "用法: $0 \"<内容>\" <来源类型> [标签1,标签2,...] [标题] [仓库路径]"
    echo "来源类型: conversation, research, generated, report"
    exit 1
fi

CONTENT="$1"
SOURCE_TYPE="$2"
TAGS="${3:-}"
TITLE="${4:-}"
VAULT_PATH="${5:-}"

# 使用 Python 脚本添加知识
if [ -n "$VAULT_PATH" ]; then
    python3 update_obsidian_knowledge.py --content "$CONTENT" --type "$SOURCE_TYPE" --tags "$TAGS" --title "$TITLE" --vault-path "$VAULT_PATH"
else
    python3 update_obsidian_knowledge.py --content "$CONTENT" --type "$SOURCE_TYPE" --tags "$TAGS" --title "$TITLE"
fi