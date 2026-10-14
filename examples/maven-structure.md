# Maven 知识树结构

```
Maven（构建工具 & 依赖管理工具）
│
├── 核心概念
│   ├── 项目对象模型（POM - Project Object Model）
│   ├── 坐标系统（GAV：GroupId, ArtifactId, Version）
│   ├── 生命周期（Lifecycle）
│   ├── 插件（Plugin）
│   └── 仓库（Repository）
│
├── 项目结构 ★ 起点
│   ├── 标准目录布局（Convention over Configuration）
│   │   ├── src/main/java（源代码）
│   │   ├── src/main/resources（资源文件）
│   │   ├── src/test/java（测试代码）
│   │   └── target/（编译输出）
│   ├── pom.xml（项目配置文件）
│   └── 多模块项目（Multi-module）
│
├── 依赖管理
│   ├── 依赖声明（<dependencies>）
│   ├── 依赖范围（Scope：compile, test, provided, runtime）
│   ├── 依赖传递（Transitive Dependencies）
│   ├── 依赖冲突解决
│   └── 依赖排除（<exclusions>）
│
├── 构建生命周期
│   ├── clean（清理）
│   ├── default（默认：compile, test, package, install, deploy）
│   ├── site（站点生成）
│   └── 阶段（Phase）vs 目标（Goal）
│
└── 仓库系统
    ├── 本地仓库（~/.m2/repository）
    ├── 中央仓库（Maven Central）
    ├── 远程仓库（私有仓库、镜像）
    └── 仓库搜索顺序
```
