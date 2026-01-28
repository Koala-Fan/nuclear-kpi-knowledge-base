#!/usr/bin/env python3
"""
简化版：向 Obsidian 仓库添加知识条目
适用于您在手机上已设置的 iCloud Obsidian 仓库
"""

import os
from datetime import datetime
from pathlib import Path


def add_simple_entry(content, entry_type="general", tags=None, title=None):
    """
    向 Obsidian 仓库添加简单条目
    """
    if tags is None:
        tags = []
    
    # 使用 iCloud 中的 Obsidian 路径
    obsidian_path = Path("~/Library/Mobile Documents/com~apple~CloudDocs/Obsidian").expanduser()
    
    # 验证仓库是否存在
    if not obsidian_path.exists():
        print(f"错误: 未找到 Obsidian 仓库在 {obsidian_path}")
        print("请确认您已在手机上正确设置仓库")
        return False
    
    # 确定目标目录
    if entry_type in ['conversation', 'chat']:
        target_dir = obsidian_path / "Conversations"
    elif entry_type in ['research', 'study']:
        target_dir = obsidian_path / "Research"
    elif entry_type in ['generated', 'ai']:
        target_dir = obsidian_path / "Generated"
    elif entry_type in ['report', 'writing']:
        target_dir = obsidian_path / "Reports"
    else:
        target_dir = obsidian_path / "Conversations"  # 默认目录
    
    # 确保目标目录存在
    target_dir.mkdir(exist_ok=True)
    
    # 创建文件名
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S.%f")[:-3]
    filename = f"entry_{timestamp}.md"
    filepath = target_dir / filename
    
    # 创建带有 Front Matter 的内容
    tags_str = " ".join([f"#{tag.strip()}" for tag in tags]) if tags else ""
    
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


# 如果直接运行此脚本
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python simple_add_to_obsidian.py <内容> [类型] [标签,用,逗号,分隔] [标题]")
        print("类型选项: conversation, research, generated, report (默认: general)")
        sys.exit(1)
    
    content = sys.argv[1]
    entry_type = sys.argv[2] if len(sys.argv) > 2 else "general"
    tags_str = sys.argv[3] if len(sys.argv) > 3 else ""
    title = sys.argv[4] if len(sys.argv) > 4 else None
    
    tags = [tag.strip() for tag in tags_str.split(",")] if tags_str else []
    
    success = add_simple_entry(content, entry_type, tags, title)
    if not success:
        sys.exit(1)