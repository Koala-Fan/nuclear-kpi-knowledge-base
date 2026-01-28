#!/usr/bin/env python3
"""
核电与考核管理知识库专用管理器
用于分类存储核电和考核相关的知识条目
"""

import os
from datetime import datetime
from pathlib import Path


class NuclearPerformanceManager:
    def __init__(self, base_dir="knowledge_base/nuclear_performance"):
        self.base_dir = Path(base_dir)
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保核电考核知识库目录结构"""
        # 核电专业领域
        nuclear_categories = [
            '核电技术体系', '核电法规标准', '核电运营管理', 
            '核电安全体系', '核电质量保证', '核电人员管理'
        ]
        
        # 考核管理领域
        kpi_categories = [
            '考核理论方法', '考核指标体系', '考核流程管理', 
            '考核工具技术', '考核改进提升'
        ]
        
        # 核电考核交叉应用
        cross_categories = [
            '核电安全考核', '核电运营考核', '核电技术考核', 
            '核电人员考核', '核电综合考核'
        ]
        
        all_categories = nuclear_categories + kpi_categories + cross_categories
        
        for category in all_categories:
            (self.base_dir / category).mkdir(parents=True, exist_ok=True)
    
    def add_knowledge(self, content, category, tags=None, title=None):
        """添加核电考核相关知识"""
        if tags is None:
            tags = []
        
        # 验证分类是否有效
        valid_categories = [
            '核电技术体系', '核电法规标准', '核电运营管理', 
            '核电安全体系', '核电质量保证', '核电人员管理',
            '考核理论方法', '考核指标体系', '考核流程管理', 
            '考核工具技术', '考核改进提升',
            '核电安全考核', '核电运营考核', '核电技术考核', 
            '核电人员考核', '核电综合考核'
        ]
        
        if category not in valid_categories:
            raise ValueError(f"无效的分类: {category}")
        
        # 创建文件名
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{title or '未命名条目'}_{timestamp}.md"
        filepath = self.base_dir / category / filename
        
        # 创建内容
        tags_str = " ".join([f"#{tag}" for tag in tags]) if tags else ""
        
        content_with_metadata = f"""# {title or '未命名条目'}

**分类**: {category}
**添加时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**标签**: {', '.join(tags) if tags else '无'}

{content}

{tags_str}
"""
        
        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content_with_metadata)
        
        print(f"核电考核知识条目已保存至: {filepath}")
        return str(filepath)


def main():
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python nuclear_performance_manager.py <内容> <分类> [标签1,标签2,...] [标题]")
        print("\n核电专业领域分类:")
        nuclear_cats = [
            '核电技术体系', '核电法规标准', '核电运营管理', 
            '核电安全体系', '核电质量保证', '核电人员管理'
        ]
        for cat in nuclear_cats:
            print(f"  - {cat}")
        
        print("\n考核管理领域分类:")
        kpi_cats = [
            '考核理论方法', '考核指标体系', '考核流程管理', 
            '考核工具技术', '考核改进提升'
        ]
        for cat in kpi_cats:
            print(f"  - {cat}")
        
        print("\n核电考核交叉应用分类:")
        cross_cats = [
            '核电安全考核', '核电运营考核', '核电技术考核', 
            '核电人员考核', '核电综合考核'
        ]
        for cat in cross_cats:
            print(f"  - {cat}")
        return
    
    content = sys.argv[1]
    category = sys.argv[2]
    tags_str = sys.argv[3] if len(sys.argv) > 3 else ""
    title = sys.argv[4] if len(sys.argv) > 4 else None
    
    tags = [tag.strip() for tag in tags_str.split(',')] if tags_str else []
    
    manager = NuclearPerformanceManager()
    try:
        manager.add_knowledge(content, category, tags, title)
    except ValueError as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()