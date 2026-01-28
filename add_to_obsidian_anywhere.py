#!/usr/bin/env python3
"""
通用 Obsidian 条目添加器
可在任何指定的目录中创建知识条目
"""

from datetime import datetime
import sys
import os
from pathlib import Path


def add_entry_to_directory(content, target_dir, entry_type="general", tags=None, title=None):
    """
    向指定目录添加条目
    """
    if tags is None:
        tags = []
    
    target_path = Path(target_dir)
    
    # 验证目标目录是否存在
    if not target_path.exists():
        print(f"错误: 目标目录不存在: {target_path}")
        return False
    
    # 确定子目录
    if entry_type in ['conversation', 'chat']:
        sub_dir = target_path / "Conversations"
    elif entry_type in ['research', 'study']:
        sub_dir = target_path / "Research"
    elif entry_type in ['generated', 'ai']:
        sub_dir = target_path / "Generated"
    elif entry_type in ['report', 'writing']:
        sub_dir = target_path / "Reports"
    else:
        sub_dir = target_path  # 默认直接在目标目录
    
    # 确保子目录存在
    sub_dir.mkdir(exist_ok=True)
    
    # 创建文件名
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S.%f")[:-3]
    filename = f"entry_{timestamp}.md"
    filepath = sub_dir / filename
    
    # 创建带有 Front Matter 的内容
    tags_str = " ".join([f"#{tag.strip()}" for tag in tags]) if tags else ""
    
    # 格式化标签数组
    tags_formatted = ', '.join([f'"{tag.strip()}"' for tag in tags]) if tags else ''
    
    content_with_frontmatter = f"""---
created: "{datetime.now().isoformat()}"
type: "{entry_type}"
tags: [{tags_formatted}]
aliases: ["{title or 'Untitled Entry'}"]
---

# {title or 'Untitled Entry'}

{content}

{tags_str}
"""
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content_with_frontmatter)
    
    print(f"条目已成功添加到: {filepath}")
    print(f"类型: {entry_type}")
    print(f"标签: {', '.join(tags) if tags else '无'}")
    return True


def main():
    if len(sys.argv) < 3:
        print("用法: python add_to_obsidian_anywhere.py <目标目录> <内容> [类型] [标签,用,逗号,分隔] [标题]")
        print("类型选项: conversation, research, generated, report (默认: general)")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    content = sys.argv[2]
    entry_type = sys.argv[3] if len(sys.argv) > 3 else "general"
    tags_str = sys.argv[4] if len(sys.argv) > 4 else ""
    title = sys.argv[5] if len(sys.argv) > 5 else None
    
    tags = [tag.strip() for tag in tags_str.split(",")] if tags_str else []
    
    success = add_entry_to_directory(content, target_dir, entry_type, tags, title)
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()