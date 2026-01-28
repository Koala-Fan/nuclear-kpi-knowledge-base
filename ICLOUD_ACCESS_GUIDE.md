# iOS 设备访问指南

## 通过 Safari 浏览知识库

### 方法一：直接访问 HTML 文件
1. 在 iPhone 上打开 "文件" App
2. 导航到 "iCloud Drive" > "knowledge_website" 文件夹
3. 点击 `index.html` 文件
4. 选择 "在 Safari 中打开"
5. 您现在可以在 Safari 中浏览整个知识库

### 方法二：使用文件 App 直接查看
1. 在 iPhone 上打开 "文件" App
2. 导航到 "iCloud Drive" > "knowledge_base" > "conversations" 等子文件夹
3. 可以直接查看 Markdown 文件
4. 对于更好的阅读体验，可以将 `.md` 文件发送到支持 Markdown 格式的阅读器

### 方法三：设置 Web 服务器（高级）
如果您有自己的 Web 服务器，可以将 `knowledge_website` 目录上传到服务器，
然后通过 URL 在任何设备上访问知识库。

## 更新知识库后
每次向知识库添加新内容后，需要重新生成网站：
```bash
python3 generate_knowledge_website.py
```

然后新内容就会出现在 iOS 设备上的知识库中。

## 注意事项
- 确保 iPhone 上的 "文件" App 已启用 iCloud Drive
- 首次访问可能需要一点时间加载
- 建议在 WiFi 环境下浏览以获得最佳体验