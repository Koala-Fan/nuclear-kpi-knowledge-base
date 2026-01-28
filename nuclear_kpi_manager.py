#!/usr/bin/env python3
"""
核电考核管理知识库专用管理器
用于分类存储核电考核相关的知识条目
"""

import os
from datetime import datetime
from pathlib import Path


class NuclearKpiManager:
    def __init__(self, base_dir="knowledge_base/nuclear_kpi"):
        self.base_dir = Path(base_dir)
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保核电考核知识库目录结构"""
        categories = [
            '法规与标准', '考核指标', '考核流程', '绩效评价', 
            '案例反馈', '风险管控', '持续改进', '数字化管理',
            '培训能力', '沟通协调'
        ]
        
        for category in categories:
            (self.base_dir / category).mkdir(parents=True, exist_ok=True)
    
    def add_knowledge(self, content, category, tags=None, title=None):
        """添加核电考核相关知识"""
        if tags is None:
            tags = []
        
        if category not in [
            '法规与标准', '考核指标', '考核流程', '绩效评价', 
            '案例反馈', '风险管控', '持续改进', '数字化管理',
            '培训能力', '沟通协调'
        ]:
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
        print("用法: python nuclear_kpi_manager.py <内容> <分类> [标签1,标签2,...] [标题]")
        print("\n可用分类:")
        categories = [
            '法规与标准', '考核指标', '考核流程', '绩效评价', 
            '案例反馈', '风险管控', '持续改进', '数字化管理',
            '培训能力', '沟通协调'
        ]
        for cat in categories:
            print(f"  - {cat}")
        return
    
    content = sys.argv[1]
    category = sys.argv[2]
    tags_str = sys.argv[3] if len(sys.argv) > 3 else ""
    title = sys.argv[4] if len(sys.argv) > 4 else None
    
    tags = [tag.strip() for tag in tags_str.split(',')] if tags_str else []
    
    manager = NuclearKpiManager()
    try:
        manager.add_knowledge(content, category, tags, title)
    except ValueError as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    main()