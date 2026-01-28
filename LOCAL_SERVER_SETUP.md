# 本地服务器设置指南

由于 GitHub 认证问题，您可以使用本地服务器来访问您的知识库：

## 启动本地服务器

运行以下命令启动本地知识库服务器：

```bash
python3 deploy_knowledge_website.py serve
```

然后在浏览器中访问：`http://localhost:8000`

## 创建启动脚本

创建一个便捷的启动脚本：

```bash
#!/bin/bash
# 启动知识库本地服务器

echo "启动核电考核管理知识库本地服务器..."

# 生成最新网站
python3 generate_knowledge_website.py

# 启动服务器
cd knowledge_website
python3 -m http.server 8000
```

保存为 `start_local_server.sh`，然后运行 `chmod +x start_local_server.sh` 给予执行权限。

## 持续使用

每次添加新知识后：
1. 使用知识管理器添加内容
2. 运行 `python3 generate_knowledge_website.py` 更新网站
3. 访问 `http://localhost:8000` 查看更新

## 在手机上访问

如果想在手机上访问：
1. 在电脑上启动本地服务器
2. 在手机上使用浏览器访问电脑的 IP 地址（如 `http://192.168.1.100:8000`）
3. 您可以在手机上将此地址添加为书签

这种方式让您能够立即使用完整的知识库系统，无需等待 GitHub 部署。