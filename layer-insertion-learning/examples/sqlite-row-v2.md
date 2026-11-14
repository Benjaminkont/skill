# 理解 SQLite 中的 Row

**学习者的疑问**：我知道 SQLite 是个数据库，表里有很多行数据，但"行"到底是什么概念？它是怎么工作的？

---

## 知识树定位

先看 Row 在 SQLite 知识树中的位置：

```
SQLite
└── Database
    └── Tables（表）
        ├── Columns（列定义）
        ├── Rows（数据行）★ 我们在这里
        ├── Indexes（索引）
        └── Triggers（触发器）
```

---

## Row 是什么

Row（行）是 SQLite 表中的一条完整记录，包含该表定义的所有列的值。

简单说：**一个 Row = 一条完整的数据记录 = 表中的一"横排"**。

例如，用户表中的一行：
```
id=1, name="张三", age=25, email="zhang@example.com"
```

---

## 同层对照：Table 中的其他组成部分

Row 在 Table 这个"房间"里，与它同层的兄弟是：

### Columns（列定义）
- **共同点**：都是 Table 的直接子组件
- **分工差异**：
  - Columns 定义**结构**（有哪些字段、什么类型、什么约束）
  - Rows 是**符合这个结构的数据实例**
- **正交关系**：Columns 是"纵向的骨架"，Rows 是"横向的内容"
- **对比发现**：Columns 是"静态的表头"，Rows 是"动态的数据"

### Indexes（索引）
- **共同点**：都属于 Table 的内部结构
- **分工差异**：
  - Indexes 是**导航结构**（B-Tree 索引树），用于快速查找 Row
  - Rows 是**被导航的目标**，是实际数据
- **协作关系**：Index 存储"某列的值 → 对应 Row 的位置"
- **对比发现**：Index 是"书的目录"，Row 是"书的正文"

### Triggers（触发器）
- **共同点**：都是 Table 的组成要素
- **分工差异**：
  - Triggers 是**规则**（当 Row 插入/更新/删除时自动执行的动作）
  - Rows 是**触发规则的对象**
- **关系**：Triggers 监听 Row 的变化并做出反应
- **对比发现**：Triggers 是"自动化脚本"，Rows 是"脚本监控的对象"

**通过同层对照理解到**：在 Table 这个容器中，Row 是"数据层"，Columns 是"结构定义"，Indexes 是"加速工具"，Triggers 是"自动化规则"。Row 既要符合 Columns 的定义，又会被 Indexes 引用，还可能触发 Triggers。

---

## 跨系统类比：从 Excel 看 Row

在 Excel 电子表格中，**一行数据**与 SQLite 的 Row 非常相似：

- 都是横向排列的一组单元格
- 都有固定的列结构（第一列是什么，第二列是什么）
- 都可以添加、删除、修改

**关键差异**：
- Excel 的行靠**行号**区分（行号会变，删除第 2 行后第 3 行变成第 2 行）
- SQLite 的 Row 有**主键/ROWID**（唯一且不变）
- Excel 可以随意编辑，SQLite 的 Row 受**约束限制**（唯一性、外键、检查约束）
- Excel 是单机文件，SQLite 的 Row 操作受**事务和锁**保护

⚠️ **不能照搬**：Excel 是"看见的就是全部"，SQLite 的 Row 背后有 B-Tree、索引、事务、锁等机制。Row 不只是"数据的摆放方式"，而是**数据库管理的基本单元**。

**这一刻理解了什么**：SQLite 的 Row 不是简单的"一行单元格"，而是受 schema 约束、被索引引用、参与事务的**结构化数据记录**。

---

## 向上抽：谁在使用 Row

### 容器层：Table（表）
Row 必须存在于某个 Table 中，Table 定义了：
- 有哪些 Columns（列）
- 每列的类型和约束
- 主键是什么

一个 Table 可以包含零到数百万个 Row。没有 Table，Row 无处安身。

### 操作层：Query Engine（查询引擎）
当你执行 SQL 查询时，Query Engine 负责处理 Row：

```sql
SELECT * FROM users WHERE age > 18;
```

**执行过程**：
1. **Parser（解析器）**：把 SQL 语句解析成语法树
2. **Query Planner（查询规划器）**：决定如何找到符合条件的 Row
   - 全表扫描（逐个检查 Row）
   - 使用索引（快速定位 Row）
3. **Virtual Machine（虚拟机）**：执行计划，读取 Row 的数据
4. 返回符合条件的 Row 给用户

**增删改查都以 Row 为单位**：
```python
import sqlite3

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# 插入一个 Row
cursor.execute(
    "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
    ("李四", 30, "li@example.com")
)

# 查询返回多个 Row
cursor.execute("SELECT * FROM users WHERE age > 25")
rows = cursor.fetchall()  # 每个元素是一个 Row（tuple）

for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
```

### 操作层：Transaction System（事务系统）
Transaction System 保证 Row 操作的一致性：

```sql
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

- **Journal（日志）**：记录 Row 修改前的状态，崩溃时可以回滚
- **Locks（锁）**：防止多个连接同时修改同一个 Row

**理解了这一层**：Row 不是孤立的数据，而是被 Query Engine 读取、被 Transaction System 保护的**操作对象**。

---

## 向下插：Row 的内部结构

### 物理存储：B-Tree Cell

SQLite 把 Row 存储在 **B-Tree** 结构中：

```
Table 的 B-Tree
├── Page 1
│   ├── Cell 1: [ROWID=1] → [1, "张三", 25, "zhang@example.com"]
│   ├── Cell 2: [ROWID=2] → [2, "李四", 30, "li@example.com"]
│   └── Cell 3: [ROWID=3] → [3, "王五", 22, "wang@example.com"]
└── Page 2
    └── ...
```

- 每个 **Row** 对应一个 **B-Tree Cell**
- Cell 存储在磁盘的 **Page**（页）中，通常一页 4KB
- B-Tree 按 ROWID 排序，支持快速查找

### ROWID（隐藏主键）

SQLite 自动为每个 Row 分配一个隐藏的 `ROWID`：
- 64 位整数
- 表中唯一
- 如果你定义了 `INTEGER PRIMARY KEY`，它就是 ROWID 的别名

```sql
-- 查看 ROWID
SELECT rowid, * FROM users;

-- 输出：
-- rowid | id | name  | age
-- ------|----+-------+----
--   1   | 1  | 张三   | 25
--   2   | 2  | 李四   | 30
```

**为什么需要 ROWID**：
- B-Tree 的键（用于快速定位 Row）
- 更新和删除时定位 Row
- 即使你没定义主键，SQLite 也能唯一标识每个 Row

### Record Format（二进制编码）

每个 Row 的数据被编码成紧凑的二进制格式：

```
[Header] [Column1] [Column2] [Column3] ...
```

**Header（头部）**：
- 变长编码，记录每列的类型和长度
- 例如：`03 05 15 0B` 表示 4 列，类型分别是 NULL、整数、文本、实数

**Column 数据**：
- 按顺序存储
- 类型可以是：NULL、INTEGER、REAL、TEXT、BLOB
- SQLite 的"动态类型"：同一列在不同 Row 可以是不同类型（虽然不推荐）

**为什么这样设计**：
- **紧凑**：变长编码让小数据占用小空间（NULL 只占 1 字节）
- **顺序访问**：读取一个 Row 时，数据在磁盘上连续排列
- **灵活**：支持动态类型系统

---

## 向下插：Row 的生命周期

### 插入 Row
```sql
INSERT INTO users (name, age) VALUES ('赵六', 28);
```

1. SQLite 分配新的 ROWID（通常是表中最大 ROWID + 1）
2. 把 Row 数据按 Record Format 编码成二进制
3. 在 B-Tree 中找到合适位置插入（按 ROWID 排序）
4. 更新相关 Indexes
5. 写入 Journal（事务日志）

### 删除 Row
```sql
DELETE FROM users WHERE id = 2;
```

1. 通过索引或全表扫描找到 ROWID = 2 的 Row
2. 从 B-Tree 中移除这个 Cell
3. 更新相关 Indexes
4. 空间标记为可复用，但不立即回收（需要 `VACUUM`）

### 更新 Row
```sql
UPDATE users SET age = 31 WHERE id = 2;
```

1. 找到目标 Row
2. 如果新数据能放在原位置，就地更新
3. 如果新数据更大，移动到新位置（ROWID 不变）
4. 更新相关 Indexes
5. 写入 Journal

**这一刻理解了什么**：Row 不是"内存中的对象"，而是磁盘上 B-Tree 中的一个 Cell，由 ROWID 索引，以紧凑的二进制格式存储。

---

## 总结：Row 的本质

**Row 是 SQLite 中"数据的完整单元"，既是逻辑上的一条记录，也是物理上 B-Tree 中的一个 Cell**。

- **逻辑层面**：一个 Row = 一条记录 = 所有列的值
- **物理层面**：一个 Row = 一个 B-Tree Cell，由 ROWID 索引
- **操作层面**：增删改查的基本单位

在 Table 这个"房间"里，Row 与 Columns、Indexes、Triggers 是同层兄弟：
- Columns 定义结构
- Indexes 加速查找
- Triggers 自动响应
- **Rows 是实际的数据**

设计动机：让数据既能高效存储（B-Tree、紧凑编码），又能灵活查询（索引、扫描），还能保证一致性（事务、日志）。

---

## 常见误区

❌ "Row 就是一行文本" → 不对，Row 是二进制编码的结构化数据  
❌ "删除 Row 就释放了空间" → 不对，需要 VACUUM 才能回收  
❌ "Row 的顺序和插入顺序相同" → 不对，Row 按 ROWID 排序，不是插入顺序  
❌ "一个 Row 就是一个 Python tuple" → 部分对，编程语言返回的是 tuple，但底层是 B-Tree Cell

**正确理解**：Row 是数据库的"原子"——不可再分的最小数据单元，既有逻辑意义（一条记录），又有物理实现（B-Tree Cell + ROWID + Record Format）。
