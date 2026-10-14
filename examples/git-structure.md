# Git 知识树结构

> 完整的 Git 命令知识树，用于层插学习法的起点定位

## 完整结构

```
Git（版本控制系统）
│
├── 初始化与配置
│   ├── git init
│   ├── git clone
│   └── git config
│
├── 工作区管理
│   ├── git status（查看状态）
│   ├── git add（暂存更改）
│   ├── git stash（临时保存）
│   ├── git reset（撤销更改）
│   ├── git restore（恢复文件）
│   └── git clean（清理未跟踪文件）
│
├── 提交历史
│   ├── git commit（创建提交）
│   ├── git log（查看历史）
│   ├── git show（查看提交详情）
│   ├── git diff（对比差异）
│   ├── git rebase（重写历史）
│   ├── git cherry-pick（选择性应用）
│   ├── git revert（安全撤销）
│   └── git reflog（操作历史）
│
├── 分支管理
│   ├── git branch（分支操作）
│   ├── git checkout / git switch（切换分支）
│   ├── git merge（合并分支）
│   └── git tag（标签管理）
│
├── 远程协作
│   ├── git remote（远程仓库管理）
│   ├── git fetch（获取更新）
│   ├── git pull（拉取并合并）
│   ├── git push（推送更新）
│   └── git clone（克隆仓库）
│
└── 高级操作
    ├── git bisect（二分查找问题）
    ├── git blame（查看代码作者）
    ├── git submodule（子模块管理）
    └── git worktree（工作树管理）
```

## 使用说明

### 在层插学习法中的使用

当讲解某个 Git 概念时：
1. 在讲解文档的"知识树定位"章节，**只裁取相关部分**
2. 用 ★ 标记当前的起点
3. 说明"完整树参见 git-structure.md"

### 示例：讲解 git stash

讲解文档中只显示相关部分：

```markdown
## 知识树定位

\`\`\`
Git（版本控制系统）
└── 工作区管理
    ├── git add（暂存更改）
    ├── git stash（临时保存）★ 起点
    ├── git reset（撤销更改）
    └── git clean（清理未跟踪文件）
\`\`\`

> 完整 Git 知识树参见 [git-structure.md](./git-structure.md)
```

### 示例：讲解 git commit history

```markdown
## 知识树定位

\`\`\`
Git（版本控制系统）
└── 提交历史 ★ 起点
    ├── git commit（创建提交）
    ├── git log（查看历史）
    ├── git rebase（重写历史）
    ├── git cherry-pick（选择性应用）
    └── git revert（安全撤销）
\`\`\`

> 完整 Git 知识树参见 [git-structure.md](./git-structure.md)
```

## 维护原则

- **单一真相源**：只在此文件维护完整的 Git 知识树
- **按需裁取**：讲解文档只显示相关的 1-2 层
- **动态标记**：★ 标记在讲解文档中动态添加，不固化在此文件

## 扩展方向

未来可以创建其他系统的知识树：
- `python-structure.md`：Python 语言知识树
- `react-structure.md`：React 框架知识树
- `linux-structure.md`：Linux 命令知识树

每个系统一个统一的 structure 文件，避免重复。
