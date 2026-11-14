# Git 提交历史：代码的时间线

> 用层插学习法理解 Git 提交历史

## 直接定义

**Git 提交历史（Commit History）**是 Git 中所有提交（commit）按时间和依赖关系形成的有向无环图（DAG）。每个提交都是代码在某个时刻的快照，包含了"谁、何时、为什么、改了什么"的完整记录。

---

## 知识树定位

```
Git（版本控制系统）
└── 提交历史 ★ 起点
    ├── git commit（创建提交）
    ├── git log（查看历史）
    ├── git rebase（重写历史）
    ├── git cherry-pick（选择性应用）
    └── git revert（安全撤销）
```

> 完整 Git 知识树参见 [git-structure.md](./git-structure.md)

---

## 一、同层对照：提交历史的操作们

在"提交历史"这个房间里，所有命令都在处理"已经提交的代码"，但各有分工：

| 命令 | 作用 | 是否改变历史 | 使用场景 |
|------|------|--------------|----------|
| `git commit` | 创建新提交 | ✅ 追加历史 | 保存一次有意义的代码变更 |
| `git log` | 查看历史 | ❌ 只读 | 了解项目演进、查找问题引入时间 |
| `git rebase` | 重写历史 | ✅ 改变已有提交 | 整理提交、线性化历史 |
| `git cherry-pick` | 复制提交 | ✅ 追加历史 | 把某个提交的改动应用到当前分支 |
| `git revert` | 反向提交 | ✅ 追加历史 | 安全撤销，不删除历史 |

### 核心差异

**按"是否改历史"分类**：
- **追加型**（安全）：`commit`、`cherry-pick`、`revert` — 只往后加，不改过去
- **改写型**（危险）：`rebase` — 修改已有提交，可能影响其他人
- **只读型**（最安全）：`log` — 纯查看

**按"用途"分类**：
- **创建历史**：`commit`
- **查看历史**：`log`
- **调整历史**：`rebase`（整理）、`cherry-pick`（挑选）、`revert`（撤销）

类比：
- `git commit`：拍照存档
- `git log`：翻相册
- `git rebase`：修图后重新洗照片
- `cherry-pick`：把别的相册里某张照片复制过来
- `revert`：拍一张"撤销"照片放在最后

---

## 二、向上抽：谁在使用提交历史？

### 容器层：版本控制系统

提交历史是 Git 的**核心价值**所在，它要解决的问题是：

**软件开发中的根本矛盾**：
- 代码总是在变化（新功能、bug 修复、重构）
- 但我们需要知道"任何时刻的代码是什么样的"
- 更需要知道"为什么会变成这样"

**提交历史提供的能力**：
1. **时间旅行**：回到任何历史版本
2. **问题追踪**：找到 bug 是什么时候引入的
3. **协作基础**：多人知道彼此改了什么
4. **代码考古**：理解"为什么当初这么写"

### 操作层：典型工作流

#### 场景 1：日常开发
```bash
# 创建提交
$ git add feature.js
$ git commit -m "feat: 添加用户登录功能"

# 查看历史
$ git log --oneline
a1b2c3d feat: 添加用户登录功能
e4f5g6h fix: 修复密码验证bug
i7j8k9l docs: 更新 API 文档
```

#### 场景 2：问题追踪
```bash
# 某个功能突然坏了，找出是哪次提交引入的
$ git log --oneline feature.js
# 看到这个文件的修改历史

$ git bisect start
$ git bisect bad          # 当前版本有问题
$ git bisect good a1b2c3d # 这个版本还正常
# Git 自动二分查找，找出引入问题的提交
```

#### 场景 3：历史整理
```bash
# 开发完成后，提交历史很乱，需要整理成清晰的故事线
$ git log --oneline
d1e2f3g WIP: 试验方案
c4d5e6f 修复拼写错误
a7b8c9d 功能完成
k1l2m3n 又改了一点

# 使用 rebase 整理
$ git rebase -i HEAD~4
# 把多个零碎提交合并成一个清晰的提交
```

---

## 三、跨系统对照：借其他系统理解

Git 提交历史像什么？

### 类比 1：文档的修订历史

**Google Docs / Word 的版本记录**：
- ✅ 都记录了"谁、何时、改了什么"
- ✅ 都可以回退到历史版本
- ✅ 都能对比版本差异

**但有重要差异**：
- ❌ 文档是**线性历史**，Git 是**树状/图状**（有分支和合并）
- ❌ 文档是**自动记录**每次修改，Git 是**手动提交**有意义的节点
- ❌ 文档难以"重写历史"，Git 可以用 `rebase` 调整

### 类比 2：视频编辑的时间线

**Premiere / Final Cut 的时间线**：
- ✅ 都是一串"变更"的序列
- ✅ 都可以剪切、移动、合并片段
- ✅ 都有"撤销"操作

**但有重要差异**：
- ❌ 视频时间线是**草稿**，Git 提交是**正式记录**
- ❌ 视频时间线最终导出成一个文件，Git 历史**永久保留**
- ❌ 视频编辑器的撤销是**临时栈**，Git 可以**永久回退**

### 关键洞察

Git 提交历史的特殊之处：
1. **不可变性**：每个提交一旦创建，内容由 SHA-1 哈希锁定
2. **分布式**：每个人都有完整历史副本
3. **可追溯**：任何改动都能追溯到责任人和原因

---

## 四、向下插：提交历史的内部结构

### 提交对象的组成

每个 Git 提交（commit）实际上是一个**数据结构**：

```
Commit Object (a1b2c3d)
├── tree: e4f5g6h            # 指向项目快照（目录树）
├── parent: i7j8k9l          # 指向父提交（可能有多个）
├── author: 张三 <zhang@example.com>
├── committer: 张三 <zhang@example.com>
├── timestamp: 2024-01-15 14:30:00
└── message: "feat: 添加用户登录功能"
```

### 历史链条

提交通过 **parent 指针**形成链条：

```
最新 ← ← ← ← ← ← ← ← ← 最早
  │                    │
a1b2c3d → e4f5g6h → i7j8k9l → m1n2o3p
  │         │         │         │
  └─────────┴─────────┴─────────┘
      parent 指针方向（指向过去）
```

### 分支与合并

历史不是简单的直线，而是**有向无环图（DAG）**：

```
         main
           │
    o──o──o──o          ← main 分支
        \    \
         o──o──o        ← feature 分支
              \
               o        ← 合并提交（两个 parent）
```

### 常用查看命令

```bash
# 1. 基础查看
git log                      # 详细历史
git log --oneline            # 简洁历史（一行一个提交）
git log --graph              # 图形化显示分支合并
git log --all --decorate     # 显示所有分支和标签

# 2. 过滤查看
git log -n 5                 # 只看最近 5 个提交
git log --since="2 weeks ago" # 最近两周的提交
git log --author="张三"      # 某个人的提交
git log --grep="fix"         # 提交消息包含 "fix" 的

# 3. 文件历史
git log -- file.js           # 某个文件的修改历史
git log -p file.js           # 同时显示每次的改动内容
git blame file.js            # 每一行代码是谁、何时写的

# 4. 对比查看
git log main..feature        # feature 有但 main 没有的提交
git log --left-right main...feature  # 两个分支的差异提交
```

### SHA-1 哈希的作用

每个提交的 ID（如 `a1b2c3d4e5f6...`）是根据内容计算的 **SHA-1 哈希值**：

**特性**：
- ✅ 内容相同 → 哈希相同（可以检测重复）
- ✅ 内容改变 → 哈希必然改变（防篡改）
- ✅ 全局唯一（碰撞几率极低）

**实际应用**：
```bash
# 可以用短哈希（前 7 位）引用提交
git show a1b2c3d

# 可以用相对引用
git show HEAD~2              # 当前提交的前第 2 个
git show main^               # main 分支的父提交
```

---

## 关键理解验证

### 1. 提交历史是"线性"的吗？

<details>
<summary>答案</summary>

❌ 不是！提交历史是**有向无环图（DAG）**：
- 分支会让历史**分叉**
- 合并会让历史**汇合**
- 一个提交可以有多个 parent（合并提交）
- 一个提交可以有多个 child（分支起点）

只有在没有分支、没有合并的情况下，历史才是线性的。
</details>

### 2. `git revert` 和 `git reset` 有什么区别？

<details>
<summary>答案</summary>

| | `git revert` | `git reset` |
|---|---|---|
| **原理** | 创建新提交来"反向"操作 | 移动分支指针，丢弃提交 |
| **历史** | 保留原提交，追加新的 | 删除或隐藏原提交 |
| **安全性** | ✅ 安全，适合公共分支 | ⚠️ 危险，不能用于已推送的提交 |
| **使用场景** | 撤销已发布的功能 | 本地调整、撤销未推送的提交 |

**记忆方式**：
- `revert` = "反悔"，但承认历史（像发"更正声明"）
- `reset` = "重置"，假装历史不存在（像删除记录）
</details>

### 3. 这个场景用什么命令？

> 你发现 3 天前的某次提交引入了 bug，但之后又有 10 个新提交。你想撤销那个有问题的提交，但保留后续的工作。

<details>
<summary>答案</summary>

```bash
# 用 git revert，不要用 git reset
git log --oneline           # 找到有问题的提交，比如 a1b2c3d
git revert a1b2c3d          # 创建一个新提交，反向应用那次的改动
```

**为什么不用 reset**：
- `reset` 会删除那次提交**及之后所有提交**
- `revert` 只撤销那一次，保留后续工作
</details>

---

## 总结：提交历史的位置

- **同层兄弟**：`commit`（创建）、`log`（查看）、`rebase`（重写）、`cherry-pick`（复制）、`revert`（撤销）
- **向上看**：是 Git 的核心价值，提供时间旅行、问题追踪、协作基础
- **向下看**：由提交对象、树对象、parent 指针组成的有向无环图（DAG）
- **跨系统**：像文档修订历史，但是树状的、手动的、不可变的

**核心价值**：让你能够安全地探索、回退、理解代码的演进过程。

---

## 常见陷阱

### 1. 在公共分支上 rebase
```bash
# ❌ 危险：main 分支已经被其他人拉取了
git checkout main
git rebase feature

# ✅ 安全：只 rebase 自己的 feature 分支
git checkout feature
git rebase main
```

**原因**：rebase 会改变提交的 SHA-1 哈希，其他人的历史会错乱。

### 2. 提交消息写得太随意
```bash
# ❌ 无用的消息
git commit -m "fix"
git commit -m "update"
git commit -m "aaa"

# ✅ 清晰的消息
git commit -m "fix: 修复用户登录时的 CSRF 验证错误"
git commit -m "feat: 添加用户头像上传功能"
```

**原因**：3 个月后你看 `git log`，"fix" 完全想不起来修了什么。

### 3. 忘记 parent 指针的方向
```bash
# 新手常犯的理解错误
A ← B ← C     # ❌ 以为箭头指向"新的"
A → B → C     # ❌ 以为箭头指向"旧的"

# 正确理解
C → B → A     # ✅ parent 指针指向过去
```

**parent 指针**永远指向"父提交"（更早的提交）。

---

## 最佳实践

### 1. 提交消息格式
推荐使用 **Conventional Commits** 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

例如：
```
feat(auth): 添加 JWT 令牌刷新机制

现在可以在令牌过期前自动刷新，
避免用户频繁登录。

Closes #123
```

**常用 type**：
- `feat`: 新功能
- `fix`: bug 修复
- `docs`: 文档
- `style`: 格式（不改代码逻辑）
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

### 2. 提交粒度
- ✅ 一个提交 = 一个**逻辑单元**（一个功能、一个 bug 修复）
- ❌ 不要把多个不相关的改动放在一个提交里
- ❌ 不要拆得太碎（"添加空格"单独一个提交）

### 3. 查看历史的技巧
```bash
# 图形化查看，非常直观
git log --graph --oneline --all --decorate

# 别名简化
git config --global alias.lg "log --graph --oneline --all --decorate"
# 之后只需要: git lg

# 查看某个文件的完整演化
git log -p --follow file.js
# --follow 会追踪文件重命名
```

---

**提交历史是 Git 的灵魂，每次提交都是一个故事节点。**
