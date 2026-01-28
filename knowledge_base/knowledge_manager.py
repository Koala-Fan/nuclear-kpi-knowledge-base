#!/usr/bin/env python3
"""
个人知识库管理器
用于分类、存储和检索有用信息
"""

import os
import json
from datetime import datetime
from pathlib import Path


class KnowledgeManager:
    def __init__(self, base_dir="knowledge_base", obsidian_vault=None):
        self.base_dir = Path(base_dir)
        self.obsidian_vault = Path(obsidian_vault) if obsidian_vault else None
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保必要的目录存在"""
        dirs = ['conversations', 'research', 'generated', 'reports', 'tags']
        for dir_name in dirs:
            (self.base_dir / dir_name).mkdir(exist_ok=True)
    
    def save_knowledge(self, content, source_type, tags=None, title=None):
        """
        保存知识条目到本地知识库和 Obsidian 仓库
        
        Args:
            content: 要保存的内容
            source_type: 来源类型 (conversation, research, generated, report)
            tags: 标签列表
            title: 标题（可选）
        """
        if tags is None:
            tags = []
        
        # 创建元数据
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'source_type': source_type,
            'tags': tags,
            'title': title or f"Knowledge Entry {datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
        
        # 根据来源类型选择存储位置
        subdir = self._get_subdir_for_type(source_type)
        filename = f"{metadata['timestamp'].replace(':', '-')}.md"
        filepath = subdir / filename
        
        # 准备 Obsidian 格式的 Front Matter
        front_matter = self._create_front_matter(metadata)
        
        # 写入本地知识库
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(front_matter)
            f.write(f"\n# {metadata['title']}\n\n")
            f.write(f"**Timestamp:** {metadata['timestamp']}\n")
            f.write(f"**Source Type:** {metadata['source_type']}\n\n")
            f.write(content)
        
        # 同时写入 Obsidian 仓库（如果设置了路径）
        if self.obsidian_vault and self.obsidian_vault.exists():
            obsidian_filepath = self._get_obsidian_path(source_type) / filename
            with open(obsidian_filepath, 'w', encoding='utf-8') as f:
                f.write(front_matter)
                f.write(f"\n# {metadata['title']}\n\n")
                f.write(content)
        
        # 为每个标签创建软链接（如果可能）或索引
        self._index_by_tags(filepath, tags)
        
        return str(filepath)
    
    def _create_front_matter(self, metadata):
        """创建 Obsidian 兼容的 Front Matter"""
        tags_formatted = [f"#{tag.replace(',', '').replace(' ', '-').lower()}" for tag in metadata['tags']]
        tags_line = " ".join(tags_formatted) if tags_formatted else ""
        
        # 正确格式化 tags 数组
        tags_array = [f'"{tag.strip("#")}"' for tag in tags_formatted]
        tags_array_str = ', '.join(tags_array) if tags_array else ''
        
        front_matter = f"""---
created: "{metadata['timestamp']}"
type: "{metadata['source_type']}"
tags: [{tags_array_str}]
aliases: ["{metadata['title']}"]
---

{tags_line}"""
        return front_matter
    
    def _get_obsidian_path(self, source_type):
        """获取 Obsidian 仓库中对应的目录"""
        mapping = {
            'conversation': 'Conversations',
            'research': 'Research', 
            'generated': 'Generated',
            'report': 'Reports',
            'writing': 'Reports'
        }
        subdir_name = mapping.get(source_type, 'Conversations')
        return self.obsidian_vault / subdir_name
    
    def _get_subdir_for_type(self, source_type):
        """获取对应类型的子目录"""
        mapping = {
            'conversation': 'conversations',
            'research': 'research', 
            'generated': 'generated',
            'report': 'reports',
            'writing': 'reports'
        }
        subdir_name = mapping.get(source_type, 'conversations')
        return self.base_dir / subdir_name
    
    def _index_by_tags(self, filepath, tags):
        """按标签创建索引"""
        for tag in tags:
            tag_file = self.base_dir / 'tags' / f"{tag.lower()}.txt"
            with open(tag_file, 'a', encoding='utf-8') as f:
                f.write(f"{filepath}\n")
    
    def search_by_tag(self, tag):
        """按标签搜索"""
        tag_file = self.base_dir / 'tags' / f"{tag.lower()}.txt"
        if not tag_file.exists():
            return []
        
        results = []
        with open(tag_file, 'r', encoding='utf-8') as f:
            for line in f:
                path = line.strip()
                if os.path.exists(path):
                    results.append(path)
        return results
    
    def get_recent_entries(self, count=5, source_type=None):
        """获取最近的条目"""
        if source_type:
            subdir = self._get_subdir_for_type(source_type)
            files = list(subdir.glob("*.md"))
        else:
            files = list(self.base_dir.rglob("*.md"))
        
        # 按修改时间排序
        files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return files[:count]


# 简单的命令行接口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python knowledge_manager.py <save/search> [参数]")
        sys.exit(1)
    
    km = KnowledgeManager()
    
    if sys.argv[1] == "save":
        if len(sys.argv) >= 5:
            content = sys.argv[2]
            source_type = sys.argv[3]
            tags_str = sys.argv[4]
            tags = [t.strip() for t in tags_str.split(',')] if tags_str else []
            
            filepath = km.save_knowledge(content, source_type, tags)
            print(f"知识条目已保存至: {filepath}")
        else:
            print("保存用法: python knowledge_manager.py save '<content>' <source_type> '<tag1,tag2>'")
    
    elif sys.argv[1] == "search":
        if len(sys.argv) >= 3:
            tag = sys.argv[2]
            results = km.search_by_tag(tag)
            print(f"标签 '{tag}' 的搜索结果:")
            for r in results:
                print(f"- {r}")
        else:
            print("搜索用法: python knowledge_manager.py search <tag>")