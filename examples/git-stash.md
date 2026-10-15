# Git Stash：临时保存未完成的工作

> 用层插学习法理解 git stash

## 直接定义

**git stash** 是 Git 的临时保存命令，可以把当前工作区和暂存区的未提交更改"藏起来"，让工作区恢复到干净状态，之后可以随时恢复这些更改。

---

## 知识树定位

```
Git（版本控制系统）
└── 工作区管理
    ├── git add（暂存更改）
    ├── git stash（临时保存）★ 起点
    ├── git reset（撤销更改）
    └── git clean（清理未跟踪文件）
```

> 完整 Git 知识树参见 [git-structure.md](../knowledge-networks/git-structure.md)

---

## 一、同层对照：看同房间的兄弟

在"工作区管理"这个房间里，`git stash` 和它的兄弟们都在处理"还没提交的更改"，但各有分工：

| 命令 | 作用 | 可恢复性 | 使用场景 |
|------|------|----------|----------|
| `git stash` | 临时保存，可恢复 | ✅ 完全可恢复 | 需要暂时切换工作，但改动还没完成 |
| `git add` | 标记为"准备提交" | ✅ 保留在暂存区 | 选择性提交部分文件 |
| `git reset` | 撤销暂存/提交 | ⚠️ 取决于参数 | 修正错误的暂存或提交 |
| `git clean` | 删除未跟踪文件 | ❌ 不可恢复 | 清理编译产物、临时文件 |

**核心差异**：
- `git stash`：像"保险箱"，改动可以随时取回
- `git add`：像"打包区"，标记要提交的内容
- `git reset`：像"后退键"，撤销操作
- `git clean`：像"碎纸机"，直接删除

---

## 二、向上抽：谁在使用它？

### 容器层：工作区管理系统

`git stash` 所在的"工作区管理"是为了解决这个问题：**代码写到一半时，如何应对突发任务？**

比如你正在开发新功能，突然需要：
- 修复紧急 bug（需要切换到 main 分支）
- 拉取远程更新（需要干净的工作区）
- 暂时搁置当前工作，尝试其他方案

这时候你有三个选择：
1. 提交未完成的代码（但会污染提交历史）
2. 放弃当前更改（但工作白费了）
3. **用 `git stash` 临时保存**（完美解决）

### 操作层：典型工作流

```bash
# 场景：你正在 feature 分支开发，突然需要修复 main 分支的 bug

$ git status
# 看到一堆未提交的更改

$ git stash push -m "功能开发到一半"
# 把更改藏起来

$ git checkout main
# 现在可以安全切换分支了

$ git checkout -b hotfix
# 修复 bug，提交，合并...

$ git checkout feature
# 回到原来的分支

$ git stash pop
# 恢复之前的工作，继续开发
```

---

## 三、跨系统对照：借其他系统理解

`git stash` 像什么呢？

**类比：编辑器的"草稿箱"**
- Word 中你可以把未完成的文档保存为草稿
- Photoshop 中你可以隐藏某个图层，稍后再显示
- `git stash` 就是代码的"草稿箱"

**但有重要差异**：
- ❌ 草稿箱通常只能保存一份，`git stash` 可以保存多份（栈结构）
- ❌ 草稿箱保存的是整个文档，`git stash` 只保存"改动"（diff）
- ❌ 草稿箱是长期存储，`git stash` 是短期临时方案

---

## 四、向下插：内部结构与实现

### git stash 由什么组成？

每次 `git stash` 实际上创建了**特殊的提交对象**：

```
stash@{0}（最新的 stash）
├── 工作区的更改（Commit A）
├── 暂存区的更改（Commit B）
└── 未跟踪的文件（可选，Commit C）
```

### 常用命令详解

```bash
# 1. 保存（多种方式）
git stash                    # 保存工作区和暂存区
git stash push -m "说明"     # 带说明保存
git stash push -u            # 同时保存未跟踪文件
git stash push path/to/file  # 只保存指定文件

# 2. 查看
git stash list              # 列出所有 stash
git stash show              # 查看最新 stash 的改动
git stash show stash@{1}    # 查看指定 stash

# 3. 恢复
git stash pop               # 恢复最新的 stash 并删除它
git stash apply             # 恢复最新的 stash 但保留它
git stash apply stash@{2}   # 恢复指定的 stash

# 4. 清理
git stash drop              # 删除最新的 stash
git stash drop stash@{1}    # 删除指定的 stash
git stash clear             # 删除所有 stash
```

### 实现机制

`git stash` 在幕后做了什么？

1. **创建临时提交**：把你的更改做成提交对象
2. **保存到引用**：存储在 `.git/refs/stash` 中
3. **重置工作区**：让工作区回到干净状态
4. **栈式管理**：最新的 stash 是 `stash@{0}`，之前的依次后移

---

## 关键理解验证

试着用自己的话回答：

### 1. 什么时候用 `git stash`，什么时候直接 `git commit`？

<details>
<summary>答案</summary>

- 代码已经完成、可以提交 → 用 `git commit`
- 代码写到一半，不想提交残缺代码 → 用 `git stash`
</details>

### 2. `git stash pop` 和 `git stash apply` 有什么区别？

<details>
<summary>答案</summary>

- `pop`：恢复后**删除** stash（一次性使用）
- `apply`：恢复后**保留** stash（可能还要在其他分支使用）
</details>

### 3. 这个场景该用哪个命令？

> 你在 feature 分支改了 5 个文件，但只想 stash 其中 2 个文件

<details>
<summary>答案</summary>

```bash
git stash push file1.js file2.js
```
</details>

---

## 总结：Git Stash 的位置

- **同层兄弟**：与 `git add`、`git reset` 一起管理工作区
- **向上看**：属于 Git 的工作区管理系统，解决"任务切换"问题
- **向下看**：内部是特殊的提交对象，栈式存储
- **跨系统**：像编辑器的草稿箱，但支持多版本、只存差异

**核心价值**：让你可以安全地中断当前工作，处理其他事情，然后无缝恢复。

---

## 常见陷阱

1. **stash 后忘记 pop/apply**：stash 会一直保留，容易积累很多无用的 stash
2. **pop 时有冲突**：如果工作区在 stash 后又修改了同样的地方，pop 时会产生合并冲突
3. **误用 clear**：`git stash clear` 会删除所有 stash，无法恢复

**最佳实践**：
- 给每个 stash 加说明：`git stash push -m "具体说明"`
- 定期清理：`git stash list` 查看，`git stash drop` 删除不需要的
- 重要改动别只靠 stash：stash 是临时方案，重要代码还是要提交
