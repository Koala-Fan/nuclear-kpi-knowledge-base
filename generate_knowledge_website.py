#!/usr/bin/env python3
"""
将知识库转换为静态网站，便于在iOS设备上浏览
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import html


def generate_html_page(content, title="知识库条目"):
    """生成单个HTML页面"""
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3 {{
            color: #2c3e50;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 14px;
        }}
        code {{
            background-color: #f1f2f3;
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 14px;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-left: 0;
            color: #666;
        }}
        .metadata {{
            background-color: #e8f4fd;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .tag {{
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin: 2px;
            text-decoration: none;
        }}
        .nav-links {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
        a {{ color: #3498db; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    {content}
</body>
</html>"""
    return html_content


def markdown_to_html(md_content):
    """简单的Markdown转HTML转换器"""
    import re
    
    html_content = md_content
    
    # 处理标题
    html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
    
    # 处理粗体
    html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
    
    # 处理元数据行
    html_content = re.sub(r'\*\*([^*]+):\*\* (.+)', r'<div><strong>\1:</strong> \2</div>', html_content)
    
    # 处理换行
    html_content = html_content.replace('\n\n', '</p><p>')
    html_content = f'<p>{html_content}</p>'
    
    # 清理多余的标签
    html_content = html_content.replace('<p></p>', '')
    
    return html_content


def generate_website():
    """生成完整的静态网站"""
    # 创建网站目录
    website_dir = Path("knowledge_website")
    website_dir.mkdir(exist_ok=True)
    
    # 复制知识库文件
    knowledge_dir = Path("knowledge_base")
    
    # 为每个知识条目生成HTML页面
    entry_count = 0
    # 遍历所有子目录，包括新的核电考核分类
    for subdir in knowledge_dir.iterdir():
        if not subdir.is_dir():
            continue
            
        # 遍历子目录下的所有MD文件（包括子子目录）
        for md_file in subdir.rglob("*.md"):  # 使用 rglob 来递归查找所有子目录中的MD文件
            # 读取Markdown内容
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # 提取标题
            title_match = re.search(r'^# (.+)', md_content, re.MULTILINE)
            title = title_match.group(1) if title_match else md_file.stem
            
            # 转换为HTML
            html_body = markdown_to_html(md_content)
            
            # 生成完整HTML页面
            html_page = generate_html_page(html_body, title)
            
            # 保存HTML文件，使用子目录名称前缀，处理中文路径
            relative_path = md_file.relative_to(knowledge_dir)
            html_filename_parts = []
            for part in relative_path.parts[:-1]:  # 除文件名外的所有部分
                html_filename_parts.append(part)
            html_filename_parts.append(md_file.name.replace('.md', '.html'))
            html_filename = '_'.join(html_filename_parts)
            
            html_path = website_dir / html_filename
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_page)
            
            entry_count += 1
    
    # 生成主页
    generate_homepage(website_dir, entry_count)
    
    print(f"静态网站已生成到 {website_dir} 目录，包含 {entry_count} 个条目")


def generate_homepage(website_dir, entry_count):
    """生成主页"""
    # 按类别组织条目
    categories = {}
    for html_file in website_dir.glob("*.html"):
        if html_file.name == "index.html":  # 排除主页自身
            continue
        
        # 提取类别（文件名的第二部分，因为现在格式是 "domain_category_title.html"）
        parts = html_file.name.split('_', 2)  # 分割最多3部分
        if len(parts) >= 2:
            category = parts[1]  # 取第二部分作为类别
        else:
            category = "其他"
        
        if category not in categories:
            categories[category] = []
        categories[category].append(html_file)
    
    homepage_content = f"""
<h1>核电与考核管理知识库</h1>

<div class="metadata">
    <p>总共 <strong>{entry_count}</strong> 个知识条目</p>
    <p>最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>

<h2>知识分类</h2>
"""

    # 为每个类别创建一个部分
    for category, files in categories.items():
        homepage_content += f"<h3>{category.replace('-', ' ').title()}</h3>\n<ul>\n"
        for html_file in files:
            link_name = html_file.name.replace('_', ' ').replace('.html', '').replace(category + ' ', '', 1).title()
            homepage_content += f'    <li><a href="{html_file.name}">{link_name}</a></li>\n'
        homepage_content += "</ul>\n"

    homepage_content += """
<div class="nav-links">
    <p><em>使用 Safari 浏览器在 iOS 设备上访问此网站</em></p>
</div>
"""
    
    # 生成主页HTML
    homepage_html = generate_html_page(homepage_content, "个人知识库")
    
    # 保存主页
    homepage_path = website_dir / "index.html"
    with open(homepage_path, 'w', encoding='utf-8') as f:
        f.write(homepage_html)


if __name__ == "__main__":
    import re  # 需要在函数外导入以供内部使用
    generate_website()
    print("知识库网站生成完成！请将 knowledge_website 目录上传到可访问的Web服务器，或通过iCloud Drive共享，在iPhone上使用Safari浏览器访问。")