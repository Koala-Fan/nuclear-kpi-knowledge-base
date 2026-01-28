#!/usr/bin/env python3
"""
知识库静态网站部署工具
"""

import http.server
import socketserver
import os
import webbrowser
import threading
from pathlib import Path


def serve_website(port=8000):
    """启动本地服务器来托管知识库网站"""
    # 切换到网站目录
    os.chdir('knowledge_website')
    
    # 创建请求处理器
    class KnowledgeRequestHandler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory='.', **kwargs)
    
    # 启动服务器
    with socketserver.TCPServer(("", port), KnowledgeRequestHandler) as httpd:
        print(f"知识库网站已在 http://localhost:{port} 启动")
        print("按 Ctrl+C 停止服务器")
        httpd.serve_forever()


def open_in_browser(port=8000):
    """在浏览器中打开网站"""
    url = f"http://localhost:{port}"
    webbrowser.open(url)


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='知识库网站部署工具')
    parser.add_argument('--port', type=int, default=8000, help='服务器端口 (默认: 8000)')
    parser.add_argument('action', choices=['serve', 'open', 'generate'], 
                       help='动作: serve(启动服务器), open(在浏览器中打开), generate(重新生成网站)')
    
    args = parser.parse_args()
    
    if args.action == 'serve':
        print(f"在端口 {args.port} 上启动知识库网站...")
        serve_website(args.port)
    elif args.action == 'open':
        print(f"在浏览器中打开 http://localhost:{args.port}")
        open_in_browser(args.port)
    elif args.action == 'generate':
        print("重新生成知识库网站...")
        import subprocess
        subprocess.run(['python3', 'generate_knowledge_website.py'])
        print("网站已重新生成")