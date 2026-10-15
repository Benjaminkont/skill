# 层插学习法 v0.5

先准备可复用的知识网络，再围绕具体对象生成完整讲义，为后续兴趣留下探索入口。

适合已经遇到某个概念、技术或现象，希望系统理解它的关系与机制。讲义覆盖同层、向上、跨系统、向下四个方向，用内容本身组织标题；没有合适内容的方向说明原因，不凑数量。方法规则以 [SKILL.md](SKILL.md) 为准。

## 仓库与产物

| 内容 | 位置与用途 |
|---|---|
| 方法 | 本目录中的 [SKILL.md](SKILL.md) |
| 共享知识网络 | [knowledge-networks/INDEX.md](../knowledge-networks/INDEX.md)：跨项目复用，持续增补 |
| 历史案例 | [examples](../examples/)：供理解讲法，保留原文，不作为 v0.5 的格式要求 |
| 演示 | [demo](../demo/) |
| 本轮讲义 | 当前工作目录的 `layer-insertion-docs/[主题].md`，用户指定位置优先 |

个人共享知识库的默认绝对路径是 `/Users/quzhong/GitHub/skill/skill/knowledge-networks/`。它与 skill 安装副本分开，避免换项目或换工具后出现多套网络。索引负责发现候选，正文负责确认范围；不能只靠文件名或关键词判断命中。

例如，“Java import”主要使用 Java 网络；跨语言代码组织问题使用代码文件管理网络；Maven 依赖管理使用 Maven 网络，并关联 Java。必要时自动补充节点或新建网络并告知；改名、合并、删除或整体重分类先讨论。

## 源码试用

本次发布只更新仓库。Codex 和 CC Switch 已安装的 skill 不会自动变成 v0.5。试用时明确引用仓库文件，例如：

```text
请使用 /Users/quzhong/GitHub/skill/skill/layer-insertion-learning/SKILL.md
用层插学习法解释 Java import，讲义保存到当前工作目录。
```

模型会先读取共享网络索引，再准备网络并保存完整讲义；对话提供概述与文件链接。需要隔离验收时，明确指定临时知识库与临时工作目录，不修改正式知识库。

## 辅助材料与冻结期

- [QUICKREF.md](QUICKREF.md)：规则摘要。
- [TEMPLATE.md](TEMPLATE.md)：可选的自然讲义示例。
- [TODO.md](TODO.md)：真实使用记录与反复出现的问题。

v0.5 收敛了网络复用、完整讲义和存储规则，取消固定层数、节点数和章节配额。场景验收通过后进入至少 5 次真实使用的冻结期，只修明确错误并正常增补网络，再依据实际问题决定是否调整方法。
