# SQLite 知识网络

范围为 SQLite 的关系数据、存储、查询与事务。与 [Qdrant](qdrant-structure.md) 可对照记录及容器关系。

```
SQLite (嵌入式关系数据库)
│
├── Database（数据库文件）
│   ├── Schema（架构）
│   │   └── Table Definitions（表定义）
│   │
│   ├── Tables（表）
│   │   ├── Columns（列定义）
│   │   ├── Rows（数据行）
│   │   ├── Indexes（索引）
│   │   └── Triggers（触发器）
│   │
│   └── Views（视图）
│
├── Storage Engine（存储引擎）
│   ├── B-Tree（B树结构）
│   ├── Page（页）
│   └── ROWID（隐藏主键）
│
├── Query Engine（查询引擎）
│   ├── Parser（解析器）
│   ├── Query Planner（查询规划器）
│   └── Virtual Machine（虚拟机）
│
└── Transaction System（事务系统）
    ├── Journal（日志）
    └── Locks（锁）
```

## 关系入口：Row

**对象**：Row（Table 的数据行）

**同层兄弟**（同在 Table 这个房间）：
- Columns（列定义）
- Indexes（索引）
- Triggers（触发器）

**向上**（容器层）：
- Table（表）

**向上**（操作层）：
- Query Engine（谁在读取 Row）
- Transaction System（谁在保证 Row 的一致性）

**向下**（内部结构）：
- B-Tree Cell（物理存储单元）
- ROWID（隐藏标识）
- Record Format（二进制编码）

**跨系统**：
- Excel 的一行
- CSV 文件的一行
