#!/usr/bin/env python3
"""
Notion 知识库集成系统
用于将对话、研究和AI生成的内容保存到 Notion 数据库
"""

import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional


class NotionKnowledgeBase:
    def __init__(self, integration_token: str = None):
        """
        初始化 Notion 知识库
        :param integration_token: Notion Integration Token
        """
        self.integration_token = integration_token or os.getenv('NOTION_TOKEN')
        self.headers = {
            'Authorization': f'Bearer {self.integration_token}',
            'Content-Type': 'application/json',
            'Notion-Version': '2022-06-28'
        }
        self.base_url = 'https://api.notion.com/v1'

    def create_database(self, parent_page_id: str, title: str = "知识库") -> str:
        """
        创建知识库数据库
        :param parent_page_id: 父页面ID
        :param title: 数据库标题
        :return: 数据库ID
        """
        url = f"{self.base_url}/databases"
        
        data = {
            "parent": {
                "type": "page_id",
                "page_id": parent_page_id
            },
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": title
                    }
                }
            ],
            "properties": {
                "Title": {
                    "title": {}
                },
                "Type": {
                    "select": {
                        "options": [
                            {
                                "name": "Conversation",
                                "color": "blue"
                            },
                            {
                                "name": "Research",
                                "color": "green"
                            },
                            {
                                "name": "Generated",
                                "color": "yellow"
                            },
                            {
                                "name": "Report",
                                "color": "purple"
                            }
                        ]
                    }
                },
                "Tags": {
                    "multi_select": {
                        "options": []
                    }
                },
                "Created": {
                    "date": {}
                },
                "Source": {
                    "rich_text": {}
                }
            }
        }

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        database_id = response.json()['id']
        print(f"数据库已创建: {database_id}")
        return database_id

    def add_entry(self, database_id: str, content: str, entry_type: str = "General", 
                  tags: List[str] = None, title: str = None, source: str = "Manual") -> str:
        """
        向数据库添加条目
        :param database_id: 数据库ID
        :param content: 内容
        :param entry_type: 条目类型
        :param tags: 标签列表
        :param title: 标题
        :param source: 来源
        :return: 页面ID
        """
        if tags is None:
            tags = []
        
        if not title:
            title = f"Entry {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        url = f"{self.base_url}/pages"
        
        # 准备标签选项
        tag_options = [{"name": tag} for tag in tags]
        
        data = {
            "parent": {
                "database_id": database_id
            },
            "properties": {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "Type": {
                    "select": {
                        "name": entry_type
                    }
                },
                "Tags": {
                    "multi_select": tag_options
                },
                "Created": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                },
                "Source": {
                    "rich_text": [
                        {
                            "text": {
                                "content": source
                            }
                        }
                    ]
                }
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": content
                                }
                            }
                        ]
                    }
                }
            ]
        }

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        page_id = response.json()['id']
        print(f"条目已添加: {page_id}")
        return page_id

    def query_database(self, database_id: str, filters: Dict = None) -> List[Dict]:
        """
        查询数据库
        :param database_id: 数据库ID
        :param filters: 过滤条件
        :return: 结果列表
        """
        url = f"{self.base_url}/databases/{database_id}/query"
        
        data = {}
        if filters:
            data["filter"] = filters

        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        
        return response.json()['results']

    def get_page(self, page_id: str) -> Dict:
        """
        获取页面详情
        :param page_id: 页面ID
        :return: 页面数据
        """
        url = f"{self.base_url}/pages/{page_id}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()


def setup_notion_integration():
    """
    设置 Notion 集成的说明
    """
    print("=== Notion 知识库设置说明 ===")
    print("\n1. 创建 Notion Integration:")
    print("   - 访问 https://www.notion.so/my-integrations")
    print("   - 点击 'New integration'")
    print("   - 输入名称（例如：Knowledge Base Assistant）")
    print("   - 选择您的 Notion 工作区")
    
    print("\n2. 获取 Integration Token:")
    print("   - 在集成页面找到 'Internal Integration Token'")
    print("   - 复制并保存此令牌")
    
    print("\n3. 共享页面给集成:")
    print("   - 在 Notion 中创建一个页面用于存放知识库")
    print("   - 点击右上角的 'Share' 按钮")
    print("   - 搜索并添加您刚创建的集成")
    print("   - 授予 'Read and write' 权限")
    
    print("\n4. 获取页面ID:")
    print("   - 打开您的知识库页面")
    print("   - 复制URL中的页面ID（URL末尾的长字符串）")
    
    print("\n5. 设置环境变量:")
    print("   - export NOTION_TOKEN='your_integration_token_here'")
    
    print("\n完成这些步骤后，系统就可以将知识条目保存到您的 Notion 空间中了。")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python notion_knowledge_base.py setup | add | query")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "setup":
        setup_notion_integration()
    elif command == "test":
        # 简单测试集成是否配置正确
        notion = NotionKnowledgeBase()
        if not notion.integration_token:
            print("错误: 未设置 NOTION_TOKEN 环境变量")
            print("请先运行: export NOTION_TOKEN='your_token_here'")
        else:
            print("Notion 集成已配置")
    else:
        print("未知命令。使用 'setup' 获取设置说明。")