# MinIO 知识树结构

```
MinIO（S3 兼容对象存储）
│
├── 存储模型
│   ├── Deployment（部署）
│   ├── Bucket（桶）
│   └── Object（对象）★ 起点
│       ├── Object Key（对象名）
│       ├── Data（对象内容）
│       ├── Metadata / Tags（元数据 / 标签）
│       └── Version（版本）
│
├── API 与工具
│   ├── S3 HTTP API
│   ├── MinIO SDK
│   └── mc Client
│
├── 管理与治理
│   ├── Policy（访问策略）
│   ├── Versioning（版本控制）
│   ├── Lifecycle（生命周期）
│   ├── Object Lock（对象锁定）
│   └── Replication（复制）
│
└── RAG 存储层
    ├── 原始文档
    ├── 解析中间产物
    ├── 图像与表格资产
    └── 回源地址（asset_uri）
```
