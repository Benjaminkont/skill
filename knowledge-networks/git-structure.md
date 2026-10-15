# Git 知识网络

当前保存 Git 命令与版本控制关系，分类供导航；整合代码时可以跨分支比较 merge、rebase、cherry-pick。

> Git 主要领域与命令关系的可增补骨架。

## 系统骨架

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

## 关系入口

- stash、add、commit 可以从“更改保存到哪里、何时形成提交”比较；stash 与工作区、暂存区和提交对象相连。
- merge、rebase、cherry-pick 可以从“如何整合代码”比较，无需修改上面的固定分类。
- 分支引用指向提交，提交连接父提交；提交历史与分支管理互相关联。
