# Git 分支合并：merge vs rebase vs cherry-pick

> 用层插学习法理解 Git 的三种分支合并方式

**🎯 强烈推荐**：先打开 [交互式可视化 Demo](../demo/git-branch-merge/index.html) 看图，再回来看文字讲解。理解 Git 分支合并，**看图比看文字重要 10 倍**。

## 直接定义

**Git 分支合并**是把不同分支的代码变更整合到一起的过程。Git 提供了三种主要方式：
- **git merge**：保留完整历史，创建合并提交
- **git rebase**：重写历史，形成线性提交
- **git cherry-pick**：精确挑选，只应用特定提交

---

## 知识树定位

```
Git（版本控制系统）
│
├── 提交历史
│   ├── git rebase（重写历史）★ 起点之一
│   └── git cherry-pick（选择性应用）★ 起点之一
│
└── 分支管理
    └── git merge（合并分支）★ 起点之一
```

> 完整 Git 知识树参见 [git-structure.md](../knowledge-networks/git-structure.md)

**为什么这三个命令分属不同的房间？**
- `merge`：属于"分支管理"，关注分支的汇合
- `rebase`、`cherry-pick`：属于"提交历史"，关注提交的操作

但它们都在解决同一个问题：**如何整合不同分支的代码**。

---

## 一、同层对照：三种合并方式的核心差异

| 命令 | 原理 | 历史结构 | 安全性 | 使用场景 |
|------|------|----------|--------|----------|
| `git merge` | 创建合并提交，保留分支 | 树状（保留分叉） | ✅ 安全 | 合并功能分支到主线 |
| `git rebase` | 重放提交，移动基点 | 线性（消除分叉） | ⚠️ 改写历史 | 整理提交、保持历史整洁 |
| `git cherry-pick` | 复制特定提交 | 追加式 | ✅ 安全 | 精确挑选某些改动 |

### 核心差异详解

#### 1. git merge：保留历史的合并

**像什么**：两条河流汇合，保留各自的来源。

```
        main
          │
    o─────o─────o─────M    ← M 是合并提交
           \         /
            o───o───o       ← feature 分支
```

**特点**：
- ✅ 保留完整历史（知道代码从哪里来）
- ✅ 安全，不改变已有提交
- ❌ 历史图复杂（多分支时很乱）
- ❌ 产生"合并提交"（额外的提交）

#### 2. git rebase：线性化的合并

**像什么**：把一条铁轨的轨道拆下来，重新铺到另一条轨道的末端。

```
合并前：
    o───o───o  main
         \
          o'──o'──o'  feature

合并后（rebase feature onto main）：
    o───o───o───o───o───o  main + feature（线性）
```

**特点**：
- ✅ 历史整洁（一条直线）
- ✅ 没有多余的合并提交
- ⚠️ 改写历史（提交 SHA 改变）
- ❌ 危险（已推送的提交不能 rebase）

#### 3. git cherry-pick：精确挑选

**像什么**：从菜单上只点你想要的菜，而不是打包全餐。

```
    o───o───o  main
         \
          A──B──C  feature

只想要 B：
    o───o───o───B'  main（只复制了 B）
```

**特点**：
- ✅ 精确控制（只要你想要的）
- ✅ 灵活（跨分支复制改动）
- ⚠️ 复制提交，不是移动（会产生重复）
- ❌ 频繁使用会让历史混乱

---

## 二、向上抽：为什么需要分支合并？

### 容器层：分支模型

分支合并是 Git **分支工作流**的核心环节，要解决的问题是：

**多人协作的根本矛盾**：
- 多个人同时开发不同功能
- 每个人在自己的分支上工作
- 最终需要把所有人的代码整合到一起

**不同合并方式适合不同的工作流**：

#### 工作流 1：Git Flow（merge 为主）
```
main ─────────M───────M────     ← 只接受合并
               │       │
develop ───M───┴───M───┴───     ← 开发主线
            │       │
feature ────┴───────┘           ← 功能分支
```
**特点**：清晰的分支层级，完整的历史追溯。

#### 工作流 2：Trunk-Based（rebase 为主）
```
main ─o─o─o─o─o─o─o─o─o─o─     ← 始终保持线性
```
**特点**：历史整洁，快速迭代，但要求高度协作。

#### 工作流 3：紧急修复（cherry-pick）
```
main ──────o─────H'             ← 从 hotfix 挑选修复
            \
hotfix ─────H                   ← 紧急修复
             \
release ─────H''                ← 也需要这个修复
```
**特点**：把一个修复应用到多个分支。

### 操作层：典型场景

#### 场景 1：功能开发完成，合并到 main（merge）
```bash
$ git checkout main
$ git merge feature

# 结果：保留 feature 分支的完整历史
```

#### 场景 2：功能开发中，同步 main 的更新（rebase）
```bash
# 在 feature 分支上
$ git rebase main

# 把 feature 的提交"移到" main 最新提交之后
```

#### 场景 3：只需要某个功能的一个修复（cherry-pick）
```bash
$ git checkout main
$ git cherry-pick abc123

# 只把提交 abc123 的改动应用过来
```

---

## 三、跨系统对照：借其他系统理解

### 类比 1：文件系统的复制 vs 移动 vs 链接

| Git 命令 | 文件操作类比 | 说明 |
|----------|--------------|------|
| `merge` | 合并文件夹（保留两个源） | 把两个文件夹的内容都保留 |
| `rebase` | 移动文件（改变位置） | 文件从 A 移到 B，不在 A 了 |
| `cherry-pick` | 复制单个文件 | 只复制你要的那一个文件 |

**但有重要差异**：
- ❌ 文件操作是物理的，Git 是基于提交历史的
- ❌ 移动文件很简单，rebase 可能产生冲突

### 类比 2：视频剪辑

| Git 命令 | 视频剪辑类比 |
|----------|--------------|
| `merge` | 画中画（两个视频同时播放） |
| `rebase` | 重新排序片段（时间线改变） |
| `cherry-pick` | 插入特定片段 |

**关键洞察**：
- `merge` 是"并行"的思维（两条线同时存在）
- `rebase` 是"串行"的思维（一条线按顺序）
- `cherry-pick` 是"选择"的思维（我只要这个）

---

## 四、向下插：内部机制与实现

### merge 的内部机制

**三方合并（3-way merge）**：
```
共同祖先：C
    │
    ├─────→ main 的最新：A
    └─────→ feature 的最新：B

合并结果：M（同时包含 A 和 B 的改动）
```

**步骤**：
1. 找到共同祖先提交（merge base）
2. 对比三方差异：C → A、C → B
3. 自动合并不冲突的部分
4. 标记冲突的部分，等待手动解决
5. 创建合并提交 M（有两个 parent：A 和 B）

### rebase 的内部机制

**重放提交（replay commits）**：
```
原来：
    C──A──B  main
    └──X──Y  feature（基于 C）

rebase 后：
    C──A──B──X'──Y'
              ↑
    feature 现在基于 B
```

**步骤**：
1. 找到共同祖先 C
2. 把 feature 的提交（X、Y）"拿出来"暂存
3. 把 feature 指针移到 main 的最新提交 B
4. 把 X、Y **重新应用**到 B 之后
5. 注意：X'、Y' 是新提交（SHA 改变了）

### cherry-pick 的内部机制

**复制提交的 diff**：
```
    o──o──o  main
        \
         A──B──C  feature

cherry-pick B：
    o──o──o──B'  main
```

**步骤**：
1. 计算提交 B 的 diff（B 的父提交 → B）
2. 把这个 diff 应用到当前分支（main）
3. 创建新提交 B'（内容一样，但 SHA 不同）

### 常用命令详解

```bash
# ===== MERGE =====
# 基础合并
git merge feature                 # 把 feature 合并到当前分支

# 禁止快进（强制创建合并提交）
git merge --no-ff feature         # 即使能快进也创建合并提交

# 快进合并（不创建合并提交）
git merge --ff-only feature       # 只在能快进时才合并

# 解决冲突
git merge feature
# 出现冲突 → 手动编辑冲突文件
git add conflicted-file.js
git commit                        # 完成合并


# ===== REBASE =====
# 基础 rebase
git checkout feature
git rebase main                   # 把 feature 的提交移到 main 之后

# 交互式 rebase（整理提交）
git rebase -i HEAD~3              # 整理最近 3 个提交
# 可以：合并提交、修改消息、删除提交、重新排序

# 继续/中止 rebase
git rebase --continue             # 解决冲突后继续
git rebase --abort                # 放弃 rebase，恢复原状


# ===== CHERRY-PICK =====
# 挑选单个提交
git cherry-pick abc123            # 把提交 abc123 应用到当前分支

# 挑选多个提交
git cherry-pick abc123 def456     # 按顺序应用

# 挑选范围（不包括起点）
git cherry-pick abc123..def456    # 应用从 abc123（不含）到 def456 的所有提交

# 只应用改动，不自动提交
git cherry-pick -n abc123         # 改动进入暂存区，需手动 commit
```

---

## 关键理解验证

### 1. merge 和 rebase 的本质区别是什么？

<details>
<summary>答案</summary>

**本质区别**：对"历史"的态度不同
- `merge`：历史是神圣的，应该**如实记录**发生了什么
- `rebase`：历史是可编辑的，应该**呈现清晰**的故事线

**技术区别**：
- `merge`：创建新提交（合并提交），不改变已有提交
- `rebase`：重写提交（改变 SHA），创造"假象"（仿佛一直在最新代码上开发）
</details>

### 2. 什么时候绝对不能用 rebase？

<details>
<summary>答案</summary>

**黄金法则：永远不要 rebase 已经推送到公共分支的提交**

❌ **危险场景**：
```bash
# main 分支已经被团队其他人拉取了
git checkout main
git rebase feature    # ❌ 灾难！其他人的历史会错乱
```

✅ **安全场景**：
```bash
# feature 是你自己的私有分支，还没推送
git checkout feature
git rebase main      # ✅ 安全，只影响你自己
```

**原因**：rebase 改变了提交的 SHA，其他人基于旧 SHA 的工作会无法合并。
</details>

### 3. 这个场景用哪个命令？

> 你在开发 feature 分支，开发了 3 天。这期间 main 分支有了 10 个新提交。现在你想：
> 1. 把 main 的新代码同步过来（避免最后合并时冲突太多）
> 2. feature 还没开发完，不能合并到 main

<details>
<summary>答案</summary>

**方案 A（推荐）：rebase**
```bash
git checkout feature
git rebase main
```
理由：feature 是私有分支，rebase 让后续合并更干净。

**方案 B（保守）：merge**
```bash
git checkout feature
git merge main
```
理由：如果 feature 已经推送且有其他人在用，不能 rebase。

**不用 cherry-pick**：cherry-pick 是精确挑选，不适合"同步全部更新"。
</details>

### 4. cherry-pick 会产生重复提交吗？

<details>
<summary>答案</summary>

**会！** cherry-pick 是**复制**提交，不是移动。

```
原来：
    main ──o──o
            \
    feature ──A──B

cherry-pick A：
    main ──o──o──A'
            \
    feature ──A──B

现在 A 和 A' 内容相同，但 SHA 不同！
```

**后果**：
- 如果后来 merge feature，会看到重复的改动（虽然 Git 能识别）
- 频繁 cherry-pick 会让历史混乱

**最佳实践**：cherry-pick 用于临时应急，不作为常规合并手段。
</details>

---

## 总结：三种方式的选择策略

### 决策树

```
需要合并分支
    │
    ├─ 是私有分支（未推送）？
    │   ├─ 是 → 想要整洁历史？
    │   │   ├─ 是 → rebase
    │   │   └─ 否 → merge
    │   └─ 否（已推送/公共分支）→ merge
    │
    └─ 只需要特定几个提交？
        └─ 是 → cherry-pick
```

### 使用场景总结

| 场景 | 推荐命令 | 原因 |
|------|----------|------|
| 功能分支合并到 main | `merge --no-ff` | 保留功能分支的完整历史 |
| 私有分支同步 main | `rebase` | 保持历史整洁，减少冲突 |
| 整理未推送的提交 | `rebase -i` | 合并零碎提交，改善提交消息 |
| 紧急修复应用到多个分支 | `cherry-pick` | 精确复制修复到需要的地方 |
| 开源项目接受 PR | `merge` 或 `rebase and merge` | 取决于项目规范 |

---

## 常见陷阱

### 1. rebase 冲突时的困惑

```bash
$ git rebase main
# 出现冲突...

# ❌ 错误：直接 commit
git add .
git commit -m "fix conflict"     # 这不会完成 rebase！

# ✅ 正确：继续 rebase
git add .
git rebase --continue            # 继续 rebase 流程
```

### 2. merge 冲突后忘记 commit

```bash
$ git merge feature
# 冲突...

# 解决冲突
$ git add .

# ❌ 忘记 commit，直接去干别的
# ✅ 必须 commit 才能完成 merge
$ git commit
```

### 3. cherry-pick 后又 merge，产生重复

```bash
# 场景：从 feature 挑了一个提交到 main
$ git checkout main
$ git cherry-pick abc123         # A' 进入 main

# 后来又 merge 整个 feature
$ git merge feature              # A 也进来了

# 结果：A 和 A' 都在历史里（虽然 Git 能处理，但很丑）
```

**避免**：cherry-pick 后，在原分支标记"已应用"，或者用 rebase 时跳过重复提交。

---

## 最佳实践

### 1. merge 的最佳实践

```bash
# 为功能分支创建有意义的合并提交
git merge --no-ff feature -m "feat: 添加用户认证模块

包含以下改动：
- JWT 令牌生成
- 登录/注册接口
- 密码加密

Closes #123"
```

### 2. rebase 的最佳实践

```bash
# rebase 前先备份
git branch feature-backup

# 交互式整理提交
git rebase -i HEAD~5
# 把多个 "WIP" 提交合并成一个有意义的提交

# 推送时需要强制（因为历史改变了）
git push --force-with-lease      # 比 --force 安全
```

### 3. cherry-pick 的最佳实践

```bash
# 挑选时保留原作者信息
git cherry-pick -x abc123        # 在提交消息中记录来源

# 批量挑选，出错时可以暂停
git cherry-pick abc123 def456
# 出现冲突 → 解决 → git cherry-pick --continue
```

---

## 可视化工具推荐

理解分支合并最好的方式是**看图**：

```bash
# 1. 内置的图形化 log
git log --graph --oneline --all --decorate

# 2. 更美观的别名
git config --global alias.tree "log --graph --oneline --all --decorate"
git tree

# 3. GUI 工具
# - GitKraken（图形化，很直观）
# - Sourcetree（免费）
# - VSCode GitLens 插件
```

---

**核心理念**：
- `merge` = 尊重历史，如实记录
- `rebase` = 整理历史，呈现清晰
- `cherry-pick` = 精确控制，按需挑选

选择哪个，取决于你的团队工作流和对历史的态度。
