# 知识库使用示例

## 添加来自对话的信息
```bash
./add_entry.sh "今天讨论了Beancount财务管理系统的使用，了解到可以将支付宝账单转换为Beancount格式" conversation "finance,beancount,alipay"
```

## 添加研究资料
```bash
./add_entry.sh "通过网络搜索了解到，Pinecone是一种优秀的向量数据库，适用于构建语义搜索功能" research "ai,search,vectordb"
```

## 添加AI生成的有价值内容
```bash
./add_entry.sh "AI建议使用多层分类系统来组织知识库，包括主题分类、时效性和重要性等级" generated "organization,ai,knowledge"
```

## 在Clawdbot中使用
在与Clawdbot的对话中，当您认为某些信息值得保存时，可以直接请求：

"请将以上信息存入知识库，标记为finance和beancount主题"

系统会自动调用知识管理脚本保存相关内容。