#!/bin/bash
# 用于将信息保存到个人知识库的便捷脚本

# 参数检查
if [ $# -lt 2 ]; then
    echo "用法: $0 \"<内容>\" <来源类型> [标签1,标签2,...]"
    echo "来源类型: conversation, research, generated, report"
    exit 1
fi

CONTENT="$1"
SOURCE_TYPE="$2"
TAGS="${3:-}"

# 使用知识管理器保存
python3 knowledge_base/knowledge_manager.py save "$CONTENT" "$SOURCE_TYPE" "$TAGS"