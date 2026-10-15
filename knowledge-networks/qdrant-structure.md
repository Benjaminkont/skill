# Qdrant 知识网络

范围为 Qdrant 的集合、记录、索引与操作。与 [SQLite](sqlite-structure.md) 可对照数据记录及容器关系，不等同其存储机制。

```
Qdrant (向量数据库)
│
├── Cluster（集群层）
│   ├── Node（节点）
│   └── Shard（分片）
│
├── Collection（集合）
│   ├── Configuration（配置）
│   │   ├── Vector Config（向量配置：维度、距离度量）
│   │   └── Optimizer Config（优化器配置）
│   │
│   ├── Points（数据层）
│   │   ├── Vector（向量）
│   │   ├── ID（标识）
│   │   └── Payload（元数据）
│   │
│   ├── Indexes（索引层）
│   │   ├── HNSW Index（图索引）
│   │   └── Payload Index（元数据索引）
│   │
│   └── Payload Schema（元数据架构）
│       └── Field Types & Indexes
│
├── Snapshot（快照）
├── Alias（别名）
│
└── API Operations（操作层）
    ├── Upsert（插入/更新）
    ├── Search（搜索）
    ├── Scroll（遍历）
    └── Delete（删除）
```

## 关系入口：Point

**对象**：Point（Collection 的数据层）

**同层兄弟**：
- Configuration（配置层）
- Indexes（索引层）
- Payload Schema（架构层）

**向上**：
- Collection（容器）
- API Operations（谁在操作 Point）

**向下**：
- Vector（向量数据）
- ID（标识符）
- Payload（元数据）

**跨系统**：
- 关系数据库的 Row
- MongoDB 的 Document
