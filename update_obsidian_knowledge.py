#!/usr/bin/env python3
"""
更新现有 Obsidian 仓库的知识库功能
此脚本将适配到您在手机上已创建的 Obsidian 仓库
"""

import os
import json
from datetime import datetime
from pathlib import Path
import argparse


def ensure_obsidian_structure(vault_path):
    """确保 Obsidian 仓库中有正确的知识库结构"""
    # 创建知识库相关目录
    dirs = ['Conversations', 'Research', 'Generated', 'Reports', 'Templates', '.obsidian']
    for dir_name in dirs:
        (vault_path / dir_name).mkdir(exist_ok=True)
    
    # 创建 Obsidian 配置文件
    obsidian_config = vault_path / '.obsidian'
    (obsidian_config / 'app.json').write_text('''{
  "showFrontmatter": true,
  "spellcheck": true,
  "foldHeading": true,
  "foldIndent": true
}''', encoding='utf-8')

    (obsidian_config / 'core-plugins.json').write_text('''{
  "graph": true,
  "backlink": true,
  "outgoing-link": true,
  "tag-pane": true,
  "page-preview": true,
  "daily-notes": true,
  "templates": true,
  "note-composer": true,
  "command-palette": true,
  "slash-command": true,
  "editor-status": true,
  "bookmarks": true,
  "outline": true,
  "word-count": true,
  "slides": false,
  "audio-recorder": false,
  "workspaces": false,
  "file-recovery": true,
  "publish": false,
  "sync": false
}''', encoding='utf-8')


def add_knowledge_to_obsidian(content, source_type, tags=None, title=None, vault_path=None):
    """
    将知识条目添加到现有的 Obsidian 仓库
    
    Args:
        content: 要保存的内容
        source_type: 来源类型 (conversation, research, generated, report)
        tags: 标签列表
        title: 标题（可选）
        vault_path: Obsidian 仓库路径
    """
    if tags is None:
        tags = []
    
    if vault_path is None:
        # 尝试找到 Obsidian 仓库
        vault_path = find_obsidian_vault()
        if vault_path is None:
            raise Exception("无法找到 Obsidian 仓库，请指定路径")
    
    # 创建元数据
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'source_type': source_type,
        'tags': tags,
        'title': title or f"Knowledge Entry {datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }
    
    # 根据来源类型选择存储位置
    mapping = {
        'conversation': 'Conversations',
        'research': 'Research', 
        'generated': 'Generated',
        'report': 'Reports',
        'writing': 'Reports'
    }
    subdir_name = mapping.get(source_type, 'Conversations')
    subdir = vault_path / subdir_name
    
    # 创建文件名
    filename = f"{metadata['timestamp'].replace(':', '-')}.md"
    filepath = subdir / filename
    
    # 准备 Obsidian 兼容的 Front Matter
    tags_formatted = [f"#{tag.replace(',', '').replace(' ', '-').lower()}" for tag in metadata['tags']]
    tags_line = " ".join(tags_formatted) if tags_formatted else ""
    
    # 格式化标签数组
    tags_array = [f'"{tag.strip("#")}"' for tag in tags_formatted]
    tags_array_str = ', '.join(tags_array) if tags_array else ''
    
    front_matter = f"""---
created: "{metadata['timestamp']}"
type: "{metadata['source_type']}"
tags: [{tags_array_str}]
aliases: ["{metadata['title']}"]
---

{tags_line}"""
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(f"\n# {metadata['title']}\n\n")
        f.write(content)
    
    print(f"知识条目已保存至: {filepath}")
    return str(filepath)


def find_obsidian_vault():
    """尝试找到 Obsidian 仓库"""
    # 检查常见的 Obsidian 仓库位置
    common_paths = [
        Path("~/Documents/ObsidianVault").expanduser(),
        Path("~/Library/Mobile Documents/com~apple~CloudDocs/Obsidian").expanduser(),
        Path("~/iCloudDrive/Obsidian").expanduser(),
    ]
    
    for path in common_paths:
        if path.exists() and (path / ".obsidian").exists():
            return path
    
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='向 Obsidian 仓库添加知识条目')
    parser.add_argument('--content', type=str, required=True, help='要保存的内容')
    parser.add_argument('--type', type=str, required=True, help='来源类型 (conversation, research, generated, report)')
    parser.add_argument('--tags', type=str, help='逗号分隔的标签列表')
    parser.add_argument('--title', type=str, help='标题')
    parser.add_argument('--vault-path', type=str, help='Obsidian 仓库路径')
    
    args = parser.parse_args()
    
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []
    
    try:
        result = add_knowledge_to_obsidian(
            content=args.content,
            source_type=args.type,
            tags=tags,
            title=args.title,
            vault_path=Path(args.vault_path) if args.vault_path else None
        )
        print(f"成功保存: {result}")
    except Exception as e:
        print(f"错误: {e}")