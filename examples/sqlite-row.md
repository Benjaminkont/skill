# 理解 SQLite 中的 Row

**学习者的疑问**：我知道 SQLite 是个数据库，表里有很多行数据，但"行"到底是什么概念？它是怎么工作的？

---

## Row 是什么

Row（行）是 SQLite 表中的一条完整记录，包含该表定义的所有列的值。

简单说：一个 Row = 一条完整的数据记录 = 表中的一"横排"。

例如，用户表中的一行：
```
id=1, name="张三", age=25, email="zhang@example.com"
```

---

## 同层对照：SQLite 中与 Row 同层的概念

### Column（列）
- **关系**：Row 和 Column 是表的两个正交维度
- **区别**：Column 定义数据的**类型和结构**（"这个表有哪些字段"），Row 是**具体的数据实例**（"这条记录的值是什么"）
- **对比**：Column 是"静态的骨架"，Row 是"动态的内容"

### Table（表）
- **关系**：Table 是 Row 的容器，一个表包含零到多个 Row
- **区别**：Table 定义了 schema（列定义、约束、索引），Row 只是其中的数据
- **类比**：Table 像表格模板，Row 像填好的一行

### Index Entry（索引条目）
- **关系**：Index Entry 是 Row 的"导航指针"
- **区别**：Index Entry 只包含被索引的列值 + Row 的位置，Row 包含完整数据
- **对比发现**：Index Entry 是为了快速查找 Row，但它本身不是 Row

通过对比，我们明确了：**Row 是表中的实际数据单元**，它既不是结构定义（Column），也不是容器（Table），更不是索引（Index Entry）。

---

## 跨系统类比：从 Excel 看 Row

在 Excel 电子表格中，**一行数据**与 SQLite 的 Row 非常相似：

- 都是横向排列的一组单元格
- 都有固定的列结构（第一列是什么，第二列是什么）
- 都可以添加、删除、修改

**关键差异**：
- Excel 的行没有唯一标识，靠行号区分（行号会变）
- SQLite 的 Row 通常有主键（唯一且不变）
- Excel 可以随意插入行，SQLite 的 Row 插入可能受约束限制（唯一性、外键等）

⚠️ **不能照搬**：Excel 是"看见的就是全部"，SQLite 的 Row 背后有索引、事务、锁等机制。Row 不只是"数据的摆放方式"，而是**数据库管理的基本单元**。

**这一刻理解了什么**：SQLite 的 Row 不是简单的"一行单元格"，而是受 schema 约束、被索引引用、参与事务的**结构化数据记录**。

---

## 向上抽：谁在使用 Row

### SQL 查询引擎
当你执行 `SELECT * FROM users WHERE age > 18` 时：

1. **扫描**：SQLite 遍历 `users` 表的所有 Row（或利用索引定位）
2. **过滤**：检查每个 Row 的 `age` 列是否满足条件
3. **返回**：把符合条件的 Row 返回给你

Row 的设计让查询引擎能够：
- **逐行处理**：不需要一次加载整个表
- **按列访问**：只读取需要的列（如果有覆盖索引）
- **快速定位**：通过 ROWID（SQLite 的隐藏列）直接跳转

### 应用层
典型使用场景：
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
rows = cursor.fetchall()  # 每个元素是一个 Row，表现为 tuple

for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")
```

理解了这一层，就明白为什么 Row 是"数据库操作的货币"——**增删改查的最小单位都是 Row**。

---

## 向下插：Row 的存储结构

SQLite 把 Row 存储在 **B-Tree** 结构中：

### 物理存储
一个表的所有 Row 存储在一棵 B-Tree 中，每个 Row 占据一个 **B-Tree Cell**：

```
[ROWID] → [Row 数据]
   1    → [1, "张三", 25, "zhang@example.com"]
   2    → [2, "李四", 30, "li@example.com"]
   3    → [3, "王五", 22, "wang@example.com"]
```

**ROWID**：
- SQLite 自动为每个 Row 分配一个隐藏的 `ROWID`（64 位整数）
- 如果你定义了 `INTEGER PRIMARY KEY`，它就是 ROWID 的别名
- ROWID 是 B-Tree 的键，Row 数据是值

### Row 的编码
每个 Row 的数据被编码成二进制格式（SQLite 的 Record Format）：

```
[header] [column1] [column2] [column3] ...
```

- **Header**：记录每列的类型和长度（变长编码，节省空间）
- **Column 数据**：按顺序存储，类型可以是 NULL、INTEGER、REAL、TEXT、BLOB

**为什么这样设计**：
- **紧凑存储**：变长编码让小数据占用小空间
- **顺序访问**：读取一个 Row 时，数据在磁盘上是连续的
- **灵活类型**：SQLite 的动态类型系统，每个 Row 的同一列可以存不同类型（虽然不推荐）

---

## 向下插：Row 的生命周期

### 插入 Row
```sql
INSERT INTO users (name, age) VALUES ('赵六', 28);
```
1. SQLite 分配新的 ROWID（通常是表中最大 ROWID + 1）
2. 把 Row 数据编码成二进制
3. 在 B-Tree 中找到合适的位置插入（按 ROWID 排序）
4. 更新相关索引（如果有）

### 删除 Row
```sql
DELETE FROM users WHERE id = 2;
```
1. 通过索引或全表扫描找到 ROWID = 2 的 Row
2. 从 B-Tree 中移除这个 Cell
3. 更新相关索引
4. 空间不会立即回收（需要 `VACUUM`）

### 更新 Row
```sql
UPDATE users SET age = 31 WHERE id = 2;
```
1. 找到目标 Row
2. 如果新数据能放在原位置，就地更新
3. 如果新数据更大，可能需要移动到新位置（ROWID 不变）
4. 更新相关索引

**这一刻理解了什么**：Row 不是"内存中的一个对象"，而是磁盘上 B-Tree 结构中的一个节点，受 ROWID 和索引的管理。

---

## 总结：Row 的本质

**Row 是 SQLite 中"数据的完整单元"，既是逻辑上的一条记录，也是物理上 B-Tree 中的一个 Cell**。

- **逻辑层面**：一个 Row = 一条记录 = 所有列的值
- **物理层面**：一个 Row = 一个 B-Tree Cell，由 ROWID 索引
- **操作层面**：增删改查的基本单位

设计动机：让数据既能高效存储（B-Tree、编码），又能灵活查询（索引、扫描）。

---

## 常见误区

❌ "Row 就是一行文本" → 不对，Row 是二进制编码的结构化数据  
❌ "删除 Row 就释放了空间" → 不对，需要 VACUUM 才能回收  
❌ "Row 的顺序和插入顺序相同" → 不对，Row 按 ROWID 排序，不是插入顺序  
❌ "一个 Row 就是一个 tuple" → 部分对，编程语言返回的是 tuple，但底层不是

**正确理解**：Row 是数据库的"原子"——不可再分的最小数据单元，既有逻辑意义（一条记录），又有物理实现（B-Tree Cell）。
