#!/usr/bin/env python3
"""
Notion 知识库辅助脚本
用于简化与 Notion 知识库的交互
"""

import sys
import os
import json
from notion_knowledge_base import NotionKnowledgeBase


def create_database(parent_page_id):
    """创建知识库数据库"""
    token = os.getenv('NOTION_TOKEN')
    if not token:
        print("错误: 未设置 NOTION_TOKEN 环境变量")
        print("请先运行: export NOTION_TOKEN='your_token_here'")
        return
    
    notion = NotionKnowledgeBase(token)
    try:
        db_id = notion.create_database(parent_page_id, "个人知识库")
        print(f"知识库数据库创建成功!")
        print(f"数据库ID: {db_id}")
        print("请保存此ID，后续添加条目时需要使用")
    except Exception as e:
        print(f"创建数据库时出错: {str(e)}")


def add_entry(database_id, content, entry_type="General", tags_str="", title=None):
    """添加知识条目"""
    token = os.getenv('NOTION_TOKEN')
    if not token:
        print("错误: 未设置 NOTION_TOKEN 环境变量")
        print("请先运行: export NOTION_TOKEN='your_token_here'")
        return
    
    # 解析标签
    tags = [tag.strip() for tag in tags_str.split(',')] if tags_str else []
    
    notion = NotionKnowledgeBase(token)
    try:
        page_id = notion.add_entry(
            database_id=database_id,
            content=content,
            entry_type=entry_type,
            tags=tags,
            title=title or f"知识条目 {entry_type}",
            source="Knowledge Assistant"
        )
        print(f"知识条目已成功添加到 Notion!")
        print(f"页面ID: {page_id}")
    except Exception as e:
        print(f"添加条目时出错: {str(e)}")


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python notion_knowledge_helper.py setup          # 显示设置说明")
        print("  python notion_knowledge_helper.py create_db <parent_page_id>  # 创建数据库")
        print("  python notion_knowledge_helper.py add <db_id> <content> <type> [tags] [title]  # 添加条目")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "setup":
        from notion_knowledge_base import setup_notion_integration
        setup_notion_integration()
    elif command == "create_db":
        if len(sys.argv) < 3:
            print("用法: python notion_knowledge_helper.py create_db <parent_page_id>")
            sys.exit(1)
        create_database(sys.argv[2])
    elif command == "add":
        if len(sys.argv) < 5:
            print("用法: python notion_knowledge_helper.py add <db_id> <content> <type> [tags] [title]")
            print("示例: python notion_knowledge_helper.py add abc123 \"这是内容\" \"Research\" \"ai,tech\" \"AI技术研究\"")
            sys.exit(1)
        
        database_id = sys.argv[2]
        content = sys.argv[3]
        entry_type = sys.argv[4]
        tags = sys.argv[5] if len(sys.argv) > 5 else ""
        title = sys.argv[6] if len(sys.argv) > 6 else None
        
        add_entry(database_id, content, entry_type, tags, title)
    else:
        print(f"未知命令: {command}")
        print("使用 'setup' 获取设置说明")


if __name__ == "__main__":
    main()