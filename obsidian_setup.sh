#!/bin/bash

# 为 Obsidian 优化知识库结构

VAULT_PATH="$HOME/Library/Mobile\ Documents/com~apple~CloudDocs/ObsidianVault"

# 创建 Obsidian vault 结构
mkdir -p "$VAULT_PATH"/{Conversations,Research,Generated,Reports,Templates,.obsidian}

# 创建 Obsidian 配置
cat > "$VAULT_PATH/.obsidian/app.json" << 'EOF'
{
  "showFrontmatter": true,
  "spellcheck": true,
  "foldHeading": true,
  "foldIndent": true
}
EOF

cat > "$VAULT_PATH/.obsidian/core-plugins.json" << 'EOF'
{
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
}
EOF

echo "Obsidian vault structure created at $VAULT_PATH"