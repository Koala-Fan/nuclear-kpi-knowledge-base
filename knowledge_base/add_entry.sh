#!/bin/bash

# 添加知识条目的便捷脚本

if [ $# -lt 2 ]; then
    echo "用法: $0 \"<内容>\" <来源类型> [标签1,标签2,...]"
    echo "来源类型: conversation, research, generated, report"
    exit 1
fi

CONTENT="$1"
SOURCE_TYPE="$2"
TAGS="${3:-}"

# 使用 Python 脚本保存知识
python3 knowledge_base/knowledge_manager.py save "$CONTENT" "$SOURCE_TYPE" "$TAGS"

echo "知识条目已添加"