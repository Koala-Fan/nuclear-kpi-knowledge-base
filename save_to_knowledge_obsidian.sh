#!/bin/bash
# 用于将信息保存到个人知识库和 Obsidian 仓库的便捷脚本

# 参数检查
if [ $# -lt 2 ]; then
    echo "用法: $0 \"<内容>\" <来源类型> [标签1,标签2,...]"
    echo "来源类型: conversation, research, generated, report"
    exit 1
fi

CONTENT="$1"
SOURCE_TYPE="$2"
TAGS="${3:-}"

# 使用知识管理器保存到本地和 Obsidian
python3 -c "
from knowledge_base.knowledge_manager import KnowledgeManager
import os
vault_path = os.path.expanduser('~/Library/Mobile Documents/com~apple~CloudDocs/ObsidianVault')
km = KnowledgeManager(obsidian_vault=vault_path)
tags_list = [t.strip() for t in '$TAGS'.split(',')] if '$TAGS' else []
result = km.save_knowledge('$CONTENT', '$SOURCE_TYPE', tags_list)
print(f'知识条目已保存至: {result}')
if vault_path:
    print(f'同时已同步至 Obsidian: {os.path.join(vault_path, \"' + result.split('/')[-2] + '\", os.path.basename(result))}')
"