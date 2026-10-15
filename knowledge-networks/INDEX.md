# 知识网络索引

按系统或稳定主题积累，先从名称、别名和问题范围选择候选，再阅读正文确认。文件名保持稳定；相同术语可能出现在不同网络，不能仅凭关键词重合判定命中。网络正文保存知识关系，本轮起点与讲解路线放在讲义中。

| 名称与文件 | 别名与典型术语 | 覆盖范围 | 相关网络 |
|---|---|---|---|
| [异步编程](async-structure.md) | asynchronous、同步/异步、async/await、Promise、Future、事件循环、event loop、非阻塞 I/O | 等待、任务执行模型及其运行时机制；语言自身的模块或包规则另按语言网络理解 | 暂无已建立的相关网络 |
| [Git](git-structure.md) | 版本控制、stash、暂存、commit、提交历史、branch、merge、rebase、cherry-pick、整合代码 | Git 内的工作区、提交、分支及协作关系 | 暂无已建立的相关网络 |
| [Qdrant](qdrant-structure.md) | 向量数据库、Point、Points、Collection、Vector、Payload、HNSW | Qdrant 的记录、集合、索引和操作 | [SQLite](sqlite-structure.md) |
| [SQLite](sqlite-structure.md) | 嵌入式数据库、Row、Rows、Table、B-Tree、ROWID、事务 | SQLite 内的关系数据、存储、查询和事务 | [Qdrant](qdrant-structure.md) |
| [Java](java-structure.md) | Java package、Java import、包、导入、全限定名、类管理、classpath、javac、JVM | Java 自身的类型、名称解析、类、包与编译运行；跨语言组织比较及 Maven 细节使用相关网络 | [代码文件管理](code-file-management-structure.md)、[Maven](maven-structure.md) |
| [Maven](maven-structure.md) | mvn、POM、pom.xml、GAV、dependency、依赖管理、构建、生命周期、多模块 | Maven 项目的布局、构建与依赖；Java 名称解析归 Java 网络 | [Java](java-structure.md)、[代码文件管理](code-file-management-structure.md) |
| [代码文件管理](code-file-management-structure.md) | 代码组织、跨语言文件管理、C++/Python/Java、include/import、头文件、模块、包 | 跨语言比较文件、代码单元、命名空间、依赖引入和编译模型；单语言细节优先匹配该语言网络 | [Java](java-structure.md)、[Maven](maven-structure.md) |

## 重叠范围怎样选

- “Java import 是什么”：主网络为 Java；需要跨语言对照时关联代码文件管理。
- “比较 C++、Python、Java 的代码组织”：主网络为代码文件管理；单独深入 Java 时沿链接继续。
- “Maven 依赖管理”：主网络为 Maven，并关联 Java；不能把 import 当作依赖下载。
- 问题跨多个网络时选最贴合当前理解目标的一份为主，链接相关网络。范围适用但缺节点时增补；没有适用范围才新建稳定主题网络并登记。

维护与讲义规则见 [SKILL.md](../layer-insertion-learning/SKILL.md)。
