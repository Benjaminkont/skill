# Maven：Java 项目的自动化管家

## 知识树定位

```
Maven（构建工具 & 依赖管理工具）
│
├── 核心概念
│   ├── 项目对象模型（POM）
│   ├── 坐标系统（GAV）
│   └── 仓库（Repository）
│
├── 项目结构 ★ 起点
│   ├── 标准目录布局
│   ├── pom.xml
│   └── target/
│
├── 依赖管理
│   ├── 依赖声明
│   ├── 依赖范围
│   └── 依赖传递
│
└── 构建生命周期
    ├── clean
    ├── compile
    ├── test
    └── package
```

> 完整知识树参见 [maven-structure.md](./maven-structure.md)

## 直接定义

**Maven** 是 Java 生态系统的**构建工具**和**依赖管理工具**。它做两件核心的事：

1. **构建管理**：自动化编译、测试、打包、部署等重复劳动
2. **依赖管理**：自动下载、管理项目需要的第三方库（jar 包）

类比：Maven 就像项目的"自动化管家"，你告诉它"我需要什么"（pom.xml），它帮你完成"下载依赖、编译代码、运行测试、打包发布"等一系列工作。

---

## 同层展开：三大 Java 构建工具对比

Maven 不是唯一的构建工具，了解它的"邻居"能更清楚它的特点。

### 1. Maven：约定优于配置

```xml
<!-- pom.xml -->
<project>
    <groupId>com.example</groupId>
    <artifactId>myapp</artifactId>
    <version>1.0.0</version>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.2.0</version>
        </dependency>
    </dependencies>
</project>
```

**特点**：
- ✅ **标准化**：统一的目录结构（src/main/java）
- ✅ **声明式**：在 XML 中声明"要什么"，Maven 自动做
- ✅ **成熟稳定**：生态最大，几乎所有 Java 库都支持
- ❌ **XML 冗长**：配置繁琐
- ❌ **灵活性较低**：自定义构建逻辑困难

### 2. Gradle：灵活且强大

```groovy
// build.gradle
plugins {
    id 'java'
}

group = 'com.example'
version = '1.0.0'

dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-web:3.2.0'
}
```

**特点**：
- ✅ **灵活**：Groovy/Kotlin DSL，编程式配置
- ✅ **性能好**：增量编译、构建缓存
- ✅ **现代化**：Android 官方构建工具
- ❌ **学习曲线陡**：需要学习 Groovy/Kotlin
- ❌ **配置复杂**：自由度高，容易配置混乱

### 3. Ant：古老的手动派

```xml
<!-- build.xml -->
<project>
    <target name="compile">
        <javac srcdir="src" destdir="build/classes"/>
    </target>
    <target name="jar" depends="compile">
        <jar destfile="myapp.jar" basedir="build/classes"/>
    </target>
</project>
```

**特点**：
- ✅ **完全控制**：手动定义每一步
- ❌ **无依赖管理**：需要手动下载 jar
- ❌ **配置繁琐**：需要写大量脚本
- ❌ **已过时**：现在很少用

### 对比表

| 维度 | Maven | Gradle | Ant |
|------|-------|--------|-----|
| **配置方式** | XML 声明式 | Groovy/Kotlin 编程式 | XML 命令式 |
| **依赖管理** | ✅ 内置 | ✅ 内置 | ❌ 需要 Ivy |
| **构建速度** | 中等 | 快（增量构建） | 慢 |
| **学习难度** | 容易 | 中等 | 容易但繁琐 |
| **生态成熟度** | 最成熟 | 成长中 | 衰退中 |
| **典型使用场景** | 企业级 Java 项目 | Android、微服务 | 遗留系统 |

**核心差异**：
- **Maven**：你描述"目标"（我要什么依赖、打什么包），Maven 按标准流程执行
- **Gradle**：你编写"脚本"（如何构建），Gradle 执行你的逻辑
- **Ant**：你编写"步骤"（先做什么、再做什么），Ant 按步骤执行

**为什么选 Maven？**
- 大多数 Java 项目的事实标准
- 新手友好：遵循约定即可
- 生态最完整：几乎所有库都有 Maven 坐标

---

## 向上抽：Maven 解决什么问题？

在没有 Maven 之前，Java 开发者面临什么困境？

### 问题 1：依赖地狱

**手动管理依赖的噩梦**：

```
你的项目需要 Spring Framework
  → 下载 spring-core.jar（10+ 个 jar 文件）
  → Spring 依赖 Apache Commons
      → 下载 commons-logging.jar
      → commons-logging 依赖 log4j
          → 下载 log4j.jar
          → log4j 依赖 ...（无穷无尽）
```

**手动操作**：
1. 去各个官网下载 jar 包
2. 检查版本兼容性（Spring 3.2 需要 Commons Logging 1.1.1）
3. 把所有 jar 复制到 `lib/` 目录
4. 在 IDE 中手动添加到 classpath
5. 同事电脑上重复一遍

**Maven 的解决方案**：

```xml
<dependencies>
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>5.3.20</version>
    </dependency>
</dependencies>
```

Maven 自动：
- ✅ 下载 spring-core.jar
- ✅ 分析它依赖什么（传递依赖）
- ✅ 递归下载所有依赖
- ✅ 处理版本冲突
- ✅ 放到本地仓库（~/.m2/repository）
- ✅ 所有开发者共享同一份配置

### 问题 2：构建流程不一致

**手动构建的混乱**：

```bash
# 开发者 A 的构建脚本
javac -d build src/**/*.java
jar cvf myapp.jar -C build .

# 开发者 B 的构建脚本
javac -sourcepath src -d out src/Main.java
jar cf app.jar -C out .

# 开发者 C 用 IDE 按钮构建，但 CI 服务器不知道怎么构建
```

**Maven 的解决方案**：

```bash
# 所有人都用同一个命令
mvn clean package
```

Maven 标准化了：
- ✅ 编译：`mvn compile`
- ✅ 测试：`mvn test`
- ✅ 打包：`mvn package`
- ✅ 安装到本地：`mvn install`
- ✅ 部署到服务器：`mvn deploy`

### 问题 3：项目结构混乱

**没有标准的噩梦**：

```
项目 A：
source/
  java/
tests/
  unit/

项目 B：
code/
  com/example/
test-code/

项目 C：
src/
  *.java
  *.properties
```

每个项目的结构不同，新人加入需要问"代码在哪？测试在哪？配置文件在哪？"

**Maven 的解决方案**：

```
任何 Maven 项目都是：
src/
  main/
    java/        ← 源代码在这
    resources/   ← 配置文件在这
  test/
    java/        ← 测试代码在这
target/          ← 编译输出在这
pom.xml          ← 项目配置在这
```

新人打开项目，立刻知道文件在哪，无需询问。

---

## 跨系统对照：C++、Python 是如何管理项目的？

了解其他语言的构建工具，能更深刻理解 Maven 的设计哲学。

### C++ 的构建世界：CMake + Conan

#### 构建工具：CMake

```cmake
# CMakeLists.txt（相当于 Maven 的 pom.xml）
cmake_minimum_required(VERSION 3.20)
project(MyApp VERSION 1.0.0)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)

# 添加可执行文件
add_executable(myapp
    src/main.cpp
    src/utils.cpp
)

# 链接库
target_link_libraries(myapp
    pthread
    boost_system
)
```

**与 Maven 的对比**：

| 维度 | Maven | CMake |
|------|-------|-------|
| **配置方式** | 声明式 XML | 脚本式（类似编程） |
| **目录结构** | 强制标准（src/main/java） | 自定义（需要手动指定） |
| **编译过程** | 自动（mvn compile） | 两步（cmake 生成 + make 编译） |
| **跨平台** | JVM 天然跨平台 | 生成平台特定的构建文件 |

**CMake 的两步构建**：
```bash
# 第 1 步：生成构建文件（生成 Makefile 或 Visual Studio 项目）
mkdir build && cd build
cmake ..

# 第 2 步：实际编译
make

# Maven 对比：一步到位
mvn compile
```

**为什么 C++ 需要两步？**
- C++ 编译器不统一（GCC、Clang、MSVC）
- 不同平台的构建系统不同（Unix 用 Makefile，Windows 用 MSBuild）
- CMake 是"构建系统的构建系统"，生成适配各平台的构建文件

**Maven 为什么一步？**
- Java 只有一个编译器（javac）
- JVM 统一了平台差异
- Maven 直接调用 javac，不需要中间层

#### 依赖管理：Conan

```python
# conanfile.txt（相当于 Maven 的 <dependencies>）
[requires]
boost/1.82.0
openssl/3.0.0
fmt/9.1.0

[generators]
CMakeDeps
CMakeToolchain
```

```bash
# 下载依赖（相当于 Maven 自动下载）
conan install . --build=missing

# 然后才能编译
cmake --preset conan-default
cmake --build build
```

**与 Maven 的对比**：

| 维度 | Maven | Conan |
|------|-------|-------|
| **依赖下载** | 自动（mvn 命令隐式） | 需要显式 `conan install` |
| **仓库** | 中央仓库统一 | ConanCenter + 自建仓库 |
| **二进制兼容** | jar 包跨平台 | 需要为每个平台/编译器构建 |
| **成熟度** | 非常成熟（20 年） | 较新（10 年） |

**C++ 依赖管理的困难**：
```
Maven：下载 Spring Boot jar → 任何平台都能用

Conan：下载 Boost
    → Windows MSVC 2022 版本
    → Linux GCC 11 版本
    → macOS Clang 14 版本
    → 需要编译或下载预编译二进制（取决于平台）
```

**为什么 C++ 这么复杂？**
- C++ 编译成机器码，不同平台不兼容
- C++ ABI 不稳定（不同编译器、不同版本可能不兼容）
- Java 的 jar 是字节码，JVM 统一执行

### Python 的构建世界：pip + poetry

#### 依赖管理：pip + requirements.txt

```bash
# requirements.txt（相当于 Maven 的 <dependencies>）
django==4.2.0
requests==2.31.0
numpy>=1.24.0,<2.0.0
```

```bash
# 安装依赖（相当于 Maven 下载 jar）
pip install -r requirements.txt

# Maven 对比
mvn dependency:resolve
```

**与 Maven 的对比**：

| 维度 | Maven | pip |
|------|-------|-----|
| **依赖声明** | pom.xml（项目元数据） | requirements.txt（纯依赖列表） |
| **版本锁定** | 精确版本 | 支持范围（>=, <） |
| **依赖隔离** | 每个项目用本地仓库 | 虚拟环境（venv） |
| **传递依赖** | 自动解析 | 自动解析 |

**Python 的虚拟环境 vs Maven 的本地仓库**：

```bash
# Python：每个项目独立的环境
python -m venv myenv
source myenv/bin/activate
pip install django  # 安装到 myenv/lib/python3.11/site-packages/

# Maven：所有项目共享本地仓库
mvn install  # 安装到 ~/.m2/repository/（全局共享）
```

**为什么 Python 需要虚拟环境？**
- Python 默认全局安装包（污染系统环境）
- 不同项目可能需要同一个库的不同版本
- 虚拟环境隔离每个项目的依赖

**Maven 为什么不需要？**
- Java 项目通过 classpath 隔离依赖
- 本地仓库只是缓存，每个项目声明自己需要哪些版本
- 运行时加载项目声明的版本，不会冲突

#### 现代 Python 项目管理：poetry

```toml
# pyproject.toml（更接近 Maven 的 pom.xml）
[tool.poetry]
name = "myapp"
version = "1.0.0"
description = "My application"

[tool.poetry.dependencies]
python = "^3.11"
django = "^4.2.0"
requests = "^2.31.0"

[tool.poetry.dev-dependencies]
pytest = "^7.4.0"
```

```bash
# 安装依赖 + 创建虚拟环境
poetry install

# 运行测试
poetry run pytest

# 构建发布包
poetry build
```

**与 Maven 的对比**：

| 维度 | Maven | poetry |
|------|-------|--------|
| **项目元数据** | ✅ groupId, artifactId, version | ✅ name, version, description |
| **依赖管理** | ✅ <dependencies> | ✅ [dependencies] |
| **测试依赖隔离** | ✅ <scope>test</scope> | ✅ [dev-dependencies] |
| **锁文件** | ❌ 没有（直接声明版本） | ✅ poetry.lock（锁定确切版本） |
| **构建命令** | mvn package | poetry build |

**poetry.lock vs Maven 的版本声明**：

```toml
# pyproject.toml：范围声明
[tool.poetry.dependencies]
requests = "^2.31.0"  # 表示 >=2.31.0, <3.0.0

# poetry.lock：锁定精确版本（自动生成）
[[package]]
name = "requests"
version = "2.31.0"  # 精确版本

[[package]]
name = "urllib3"
version = "2.0.4"   # 传递依赖也锁定
```

```xml
<!-- Maven：直接声明精确版本 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.2.0</version>  <!-- 精确版本，不是范围 -->
</dependency>
```

**为什么 Python 需要锁文件？**
- Python 社区习惯用版本范围（^2.31.0）
- 锁文件确保团队每个人安装相同版本
- 避免"在我机器上能跑"的问题

**Maven 为什么不需要？**
- Java 社区习惯声明精确版本（3.2.0）
- pom.xml 本身就是"锁文件"
- 依赖冲突通过 Maven 的仲裁机制解决

### 三种语言的对比表

| 维度 | Java (Maven) | C++ (CMake + Conan) | Python (pip/poetry) |
|------|-------------|---------------------|---------------------|
| **构建工具** | Maven | CMake | setuptools/poetry |
| **依赖管理** | Maven 内置 | Conan（独立工具） | pip（内置） |
| **配置文件** | pom.xml | CMakeLists.txt + conanfile.txt | requirements.txt / pyproject.toml |
| **仓库** | Maven Central（统一） | ConanCenter | PyPI（统一） |
| **二进制分发** | jar（跨平台字节码） | 平台特定二进制 | wheel（平台特定或纯 Python） |
| **依赖隔离** | classpath（项目级） | 不需要（编译时链接） | 虚拟环境（目录级） |
| **标准目录** | 强制（src/main/java） | 自定义 | 约定（但不强制） |
| **构建速度** | 中等 | 慢（需要编译 C++） | 快（解释型语言） |
| **学习曲线** | 容易 | 陡峭 | 容易 |

### 关键差异的根源

#### 1. 语言特性决定工具设计

**Java（编译到字节码）**：
```
Java 源码 → javac → .class 字节码 → jar 打包 → JVM 执行
                                        ↓
                                  跨平台，一次编译到处运行
```
→ Maven 可以直接分发 jar，无需考虑平台差异

**C++（编译到机器码）**：
```
C++ 源码 → g++/clang/msvc → 机器码（.o/.obj） → 链接 → 可执行文件
                                                    ↓
                                          平台特定，每个平台都要重新编译
```
→ Conan 需要为每个平台分发不同的二进制，或者分发源码（用户自己编译）

**Python（解释执行）**：
```
Python 源码 → 解释器直接执行（或编译成 .pyc）
               ↓
          跨平台（如果没有 C 扩展）
```
→ pip 可以分发纯 Python 包（.py 文件），但 C 扩展需要平台特定的 wheel

#### 2. 生态成熟度影响标准化

**Java**：
- Maven 是事实标准（20 年历史）
- 几乎所有库都在 Maven Central
- 强制标准化（目录结构、生命周期）

**C++**：
- 没有统一标准（CMake 是最流行的，但不是唯一的）
- 包管理是近 10 年才成熟（Conan、vcpkg）
- 高度灵活（每个项目可以完全自定义）

**Python**：
- pip 是事实标准（15 年历史）
- 几乎所有库都在 PyPI
- 约定优于强制（有标准目录结构，但不强制）

### 什么不能照搬？

#### ❌ 不要把 C++ 的构建复杂性带到 Java

**错误思维**：
> "CMake 需要两步构建（cmake + make），所以 Maven 也应该分成两步？"

**为什么错误**：
- C++ 需要两步是因为跨平台编译器不统一
- Java 只有一个编译器（javac），不需要生成中间构建文件

#### ❌ 不要把 Python 的虚拟环境概念带到 Java

**错误思维**：
> "Python 每个项目需要独立的虚拟环境，所以 Java 也应该为每个项目复制一份依赖？"

**为什么错误**：
- Python 虚拟环境是为了隔离全局安装的包
- Maven 的本地仓库已经是全局缓存，项目通过 pom.xml 声明使用哪些版本
- 复制依赖会浪费大量磁盘空间

#### ❌ 不要把 Maven 的强制结构带到其他语言

**错误思维**：
> "Maven 的 src/main/java 结构很好，C++ 项目也应该强制这样？"

**为什么错误**：
- C++ 生态没有统一标准，项目差异很大
- 遗留代码库、第三方库的结构无法强制改变
- CMake 的灵活性正是为了适配各种项目

### 可以借鉴的地方

#### ✅ C++ 可以学习 Maven 的依赖传递

**Conan 已经实现**：
```python
# conanfile.txt
[requires]
boost/1.82.0  # Conan 会自动下载 boost 依赖的其他库
```

#### ✅ Python 可以学习 Maven 的精确版本声明

**poetry 已经实现**：
```toml
# pyproject.toml 支持精确版本
[tool.poetry.dependencies]
django = "4.2.0"  # 精确版本（不用范围）
```

#### ✅ Java 可以学习 Python 的锁文件

**Maven 的问题**：
```xml
<!-- 使用了版本范围（不推荐，但有人这样做） -->
<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>[30.0,31.0)</version>
</dependency>
```
不同时间构建可能得到不同版本（30.0 vs 30.1.1）

**解决方案**（Gradle 已实现）：
```
gradle.lockfile  ← 锁定确切版本
```

---

## 向下插：Maven 如何工作？

现在我们知道 Maven 解决了"依赖地狱、构建混乱、结构不统一"，但它**如何做到**的？

### 核心机制 1：坐标系统（GAV）

Maven 用**唯一坐标**定位每个库：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>      <!-- G：组织/公司 -->
    <artifactId>spring-boot-starter-web</artifactId> <!-- A：具体的库 -->
    <version>3.2.0</version>                         <!-- V：版本号 -->
</dependency>
```

**GAV 坐标类比：快递地址**

```
GroupId（省市区）：    org.springframework.boot
ArtifactId（街道门牌）：spring-boot-starter-web
Version（收件人）：    3.2.0

完整坐标：org.springframework.boot:spring-boot-starter-web:3.2.0
```

**实际例子**：

| 库名 | GroupId | ArtifactId | 坐标 |
|------|---------|------------|------|
| Spring Boot Web | org.springframework.boot | spring-boot-starter-web | org.springframework.boot:spring-boot-starter-web:3.2.0 |
| JUnit 5 | org.junit.jupiter | junit-jupiter | org.junit.jupiter:junit-jupiter:5.9.0 |
| MySQL 驱动 | mysql | mysql-connector-java | mysql:mysql-connector-java:8.0.33 |
| Gson | com.google.code.gson | gson | com.google.code.gson:gson:2.10.1 |

**为什么需要 GroupId？**

```xml
<!-- Apache 的 Commons IO -->
<dependency>
    <groupId>commons-io</groupId>
    <artifactId>commons-io</artifactId>
    <version>2.11.0</version>
</dependency>

<!-- Google 也有一个叫 commons-io 的库（假设） -->
<dependency>
    <groupId>com.google.common</groupId>
    <artifactId>commons-io</artifactId>
    <version>1.0.0</version>
</dependency>
```

GroupId 确保了全球唯一性，就像 Java 的包名（com.example.util）。

### 核心机制 2：仓库系统

Maven 从哪里下载依赖？答案是**三级仓库系统**。

#### 本地仓库（~/.m2/repository）

```
~/.m2/repository/
└── org/
    └── springframework/
        └── boot/
            └── spring-boot-starter-web/
                └── 3.2.0/
                    ├── spring-boot-starter-web-3.2.0.jar      ← jar 文件
                    ├── spring-boot-starter-web-3.2.0.pom      ← 这个库的 pom
                    └── spring-boot-starter-web-3.2.0.jar.sha1 ← 校验和
```

**作用**：
- 缓存已下载的依赖
- 多个项目共享同一份 jar（节省磁盘空间）
- 离线时可用

#### 中央仓库（Maven Central）

```
https://repo.maven.apache.org/maven2/
```

**全球最大的 Java 库仓库**：
- 包含 50 万+ 开源库
- 免费、公开访问
- 镜像遍布全球（中国常用阿里云镜像）

**搜索网站**：
- https://mvnrepository.com/（推荐）
- https://search.maven.org/

#### 私有仓库（公司内部）

```xml
<repositories>
    <repository>
        <id>company-repo</id>
        <url>https://repo.mycompany.com/maven2</url>
    </repository>
</repositories>
```

**用途**：
- 托管公司内部的库
- 代理中央仓库（加速、安全）
- 常用工具：Nexus、Artifactory

#### 查找顺序

```
1. 查找本地仓库（~/.m2/repository）
   ↓ 没有
2. 查找私有仓库（如果配置了）
   ↓ 没有
3. 查找中央仓库（Maven Central）
   ↓ 下载
4. 保存到本地仓库（供下次使用）
```

**实际演示**：

```bash
# 第一次构建（本地没有依赖）
$ mvn clean package
Downloading from central: https://repo.maven.apache.org/.../spring-boot-starter-web-3.2.0.jar
Downloaded: spring-boot-starter-web-3.2.0.jar (1.2 MB)
...

# 第二次构建（本地已有依赖）
$ mvn clean package
# 不再下载，直接从本地仓库读取
```

### 核心机制 3：依赖传递

**Spring Boot Web 的依赖树**：

```
spring-boot-starter-web:3.2.0
├── spring-boot-starter:3.2.0
│   ├── spring-boot:3.2.0
│   ├── spring-boot-autoconfigure:3.2.0
│   └── logback-classic:1.4.11
│       └── slf4j-api:2.0.7
├── spring-webmvc:6.1.0
│   ├── spring-web:6.1.0
│   └── spring-context:6.1.0
└── tomcat-embed-core:10.1.15
```

**你只需要声明**：
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.2.0</version>
</dependency>
```

**Maven 自动下载**：
- spring-boot-starter-web
- 它依赖的 spring-boot-starter
- spring-boot-starter 依赖的 logback-classic
- logback-classic 依赖的 slf4j-api
- ...（递归到底）

**查看依赖树**：
```bash
$ mvn dependency:tree
[INFO] com.example:myapp:jar:1.0.0
[INFO] └── org.springframework.boot:spring-boot-starter-web:jar:3.2.0:compile
[INFO]     ├── org.springframework.boot:spring-boot-starter:jar:3.2.0:compile
[INFO]     │   ├── org.springframework.boot:spring-boot:jar:3.2.0:compile
[INFO]     │   └── ch.qos.logback:logback-classic:jar:1.4.11:compile
[INFO]     │       └── org.slf4j:slf4j-api:jar:2.0.7:compile
[INFO]     └── org.springframework:spring-webmvc:jar:6.1.0:compile
```

### 核心机制 4：构建生命周期

Maven 定义了一套**标准的构建流程**（生命周期）：

```
clean → validate → compile → test → package → verify → install → deploy
```

**每个阶段做什么**：

| 阶段 | 作用 | 命令 | 输出 |
|------|------|------|------|
| **clean** | 删除 target/ 目录 | `mvn clean` | 清空编译结果 |
| **compile** | 编译 src/main/java | `mvn compile` | target/classes/ |
| **test** | 运行测试 src/test/java | `mvn test` | 测试报告 |
| **package** | 打包成 jar/war | `mvn package` | target/myapp-1.0.0.jar |
| **install** | 安装到本地仓库 | `mvn install` | ~/.m2/repository/... |
| **deploy** | 部署到远程仓库 | `mvn deploy` | 上传到服务器 |

**关键特性：阶段是有顺序的**

```bash
mvn package
# 实际执行：validate → compile → test → package
```

你运行 `mvn package`，Maven 会自动先执行前面的所有阶段。

**常用组合**：
```bash
mvn clean package    # 先清理，再编译、测试、打包
mvn clean install    # 清理 → 打包 → 安装到本地仓库
mvn clean test       # 清理 → 编译 → 测试
```

---

## 实战案例：从零创建一个 Maven 项目

### 场景：创建一个 Spring Boot Web 应用

#### 第 1 步：创建项目结构

```bash
# 使用 Maven 命令创建项目
mvn archetype:generate \
  -DgroupId=com.example \
  -DartifactId=mywebapp \
  -DarchetypeArtifactId=maven-archetype-quickstart \
  -DinteractiveMode=false

# 生成的目录结构：
mywebapp/
├── pom.xml
└── src/
    ├── main/
    │   └── java/
    │       └── com/
    │           └── example/
    │               └── App.java
    └── test/
        └── java/
            └── com/
                └── example/
                    └── AppTest.java
```

#### 第 2 步：编辑 pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 项目坐标 -->
    <groupId>com.example</groupId>
    <artifactId>mywebapp</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <!-- 项目信息 -->
    <name>My Web App</name>
    <description>A simple web application</description>

    <!-- 属性配置 -->
    <properties>
        <java.version>17</java.version>
        <spring.boot.version>3.2.0</spring.boot.version>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <!-- 依赖管理 -->
    <dependencies>
        <!-- Spring Boot Web Starter -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>${spring.boot.version}</version>
        </dependency>

        <!-- 测试依赖 -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <version>${spring.boot.version}</version>
            <scope>test</scope>  <!-- 只在测试时使用 -->
        </dependency>
    </dependencies>

    <!-- 构建配置 -->
    <build>
        <plugins>
            <!-- Spring Boot 打包插件 -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring.boot.version}</version>
            </plugin>
        </plugins>
    </build>
</project>
```

**pom.xml 结构解析**：

```xml
<project>
    <!-- 1. 项目坐标：这个项目是谁 -->
    <groupId>com.example</groupId>
    <artifactId>mywebapp</artifactId>
    <version>1.0.0</version>
    
    <!-- 2. 属性：变量定义 -->
    <properties>
        <java.version>17</java.version>
    </properties>
    
    <!-- 3. 依赖：这个项目需要什么库 -->
    <dependencies>
        <dependency>...</dependency>
    </dependencies>
    
    <!-- 4. 构建：如何编译、打包 -->
    <build>
        <plugins>
            <plugin>...</plugin>
        </plugins>
    </build>
</project>
```

#### 第 3 步：编写代码

```java
// src/main/java/com/example/App.java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class App {
    public static void main(String[] args) {
        SpringApplication.run(App.class, args);
    }
    
    @GetMapping("/")
    public String hello() {
        return "Hello, Maven!";
    }
}
```

#### 第 4 步：构建和运行

```bash
# 1. 清理并打包
$ mvn clean package

[INFO] Scanning for projects...
[INFO] 
[INFO] ----------------< com.example:mywebapp >----------------
[INFO] Building My Web App 1.0.0
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- maven-clean-plugin:3.2.0:clean (default-clean) @ mywebapp ---
[INFO] Deleting /path/to/mywebapp/target
[INFO] 
[INFO] --- maven-resources-plugin:3.3.0:resources (default-resources) @ mywebapp ---
[INFO] Copying 1 resource
[INFO] 
[INFO] --- maven-compiler-plugin:3.10.1:compile (default-compile) @ mywebapp ---
[INFO] Compiling 1 source file to /path/to/mywebapp/target/classes
[INFO] 
[INFO] --- maven-compiler-plugin:3.10.1:testCompile (default-testCompile) @ mywebapp ---
[INFO] Compiling 1 source file to /path/to/mywebapp/target/test-classes
[INFO] 
[INFO] --- maven-surefire-plugin:2.22.2:test (default-test) @ mywebapp ---
[INFO] 
[INFO] -------------------------------------------------------
[INFO]  T E S T S
[INFO] -------------------------------------------------------
[INFO] Running com.example.AppTest
[INFO] Tests run: 1, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] --- maven-jar-plugin:3.3.0:jar (default-jar) @ mywebapp ---
[INFO] Building jar: /path/to/mywebapp/target/mywebapp-1.0.0.jar
[INFO] 
[INFO] --- spring-boot-maven-plugin:3.2.0:repackage (repackage) @ mywebapp ---
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------

# 2. 查看生成的文件
$ ls target/
classes/                     # 编译后的 .class 文件
test-classes/                # 测试类
mywebapp-1.0.0.jar           # 可执行 jar（包含所有依赖）
mywebapp-1.0.0.jar.original  # 原始 jar（不含依赖）

# 3. 运行应用
$ java -jar target/mywebapp-1.0.0.jar

  .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::                (v3.2.0)

2024-01-15 10:30:00.123  INFO 12345 --- [main] com.example.App : Started App in 2.5 seconds

# 4. 测试
$ curl http://localhost:8080/
Hello, Maven!
```

---

## 依赖范围（Scope）详解

Maven 的依赖有**不同的作用范围**，控制何时使用这个依赖。

### 五种依赖范围

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <version>3.2.0</version>
    <scope>compile</scope>  <!-- 默认值 -->
</dependency>
```

| Scope | 编译时 | 测试时 | 运行时 | 打包进 jar | 典型用途 |
|-------|--------|--------|--------|-----------|---------|
| **compile** | ✅ | ✅ | ✅ | ✅ | 业务代码需要的库（默认） |
| **test** | ❌ | ✅ | ❌ | ❌ | 测试框架（JUnit） |
| **provided** | ✅ | ✅ | ❌ | ❌ | 容器提供的库（Servlet API） |
| **runtime** | ❌ | ✅ | ✅ | ✅ | 运行时需要的库（JDBC 驱动） |
| **system** | ✅ | ✅ | ❌ | ❌ | 本地 jar（不推荐） |

### 实际例子

```xml
<dependencies>
    <!-- compile：默认范围，业务代码需要 -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <version>3.2.0</version>
        <scope>compile</scope>  <!-- 可以省略，默认就是 compile -->
    </dependency>

    <!-- test：只在测试时使用 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.9.0</version>
        <scope>test</scope>
    </dependency>

    <!-- provided：编译时需要，但运行时由容器提供 -->
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>javax.servlet-api</artifactId>
        <version>4.0.1</version>
        <scope>provided</scope>  <!-- Tomcat 会提供 -->
    </dependency>

    <!-- runtime：运行时需要，但编译时不需要 -->
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>8.0.33</version>
        <scope>runtime</scope>  <!-- 代码里不直接 import MySQL 类 -->
    </dependency>
</dependencies>
```

**为什么 MySQL 驱动是 runtime？**

```java
// 你的代码只用 JDBC 标准接口（JDK 自带）
import java.sql.Connection;
import java.sql.DriverManager;

Connection conn = DriverManager.getConnection(
    "jdbc:mysql://localhost:3306/mydb",
    "user", "password"
);
// 编译时不需要 MySQL 驱动
// 运行时 DriverManager 通过反射加载 MySQL 驱动
```

---

## 依赖冲突解决

### 问题场景

```
你的项目依赖：
├── A 库（依赖 Gson 2.8.0）
└── B 库（依赖 Gson 2.10.0）

Gson 应该用哪个版本？
```

### Maven 的解决策略

#### 策略 1：最短路径优先

```
项目
├── A:1.0 → C:1.0
└── B:1.0 → D:1.0 → C:2.0

结果：使用 C:1.0（路径长度 2 < 3）
```

#### 策略 2：第一声明优先（路径相同时）

```xml
<dependencies>
    <dependency>
        <groupId>A</groupId>
        <artifactId>A</artifactId>
        <version>1.0</version>  <!-- 依赖 C:1.0 -->
    </dependency>
    <dependency>
        <groupId>B</groupId>
        <artifactId>B</artifactId>
        <version>1.0</version>  <!-- 依赖 C:2.0 -->
    </dependency>
</dependencies>

结果：使用 C:1.0（A 先声明）
```

#### 策略 3：手动排除冲突

```xml
<dependency>
    <groupId>A</groupId>
    <artifactId>A</artifactId>
    <version>1.0</version>
    <exclusions>
        <!-- 排除 A 传递的 Gson -->
        <exclusion>
            <groupId>com.google.code.gson</groupId>
            <artifactId>gson</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<!-- 手动指定想要的版本 -->
<dependency>
    <groupId>com.google.code.gson</groupId>
    <artifactId>gson</artifactId>
    <version>2.10.0</version>
</dependency>
```

### 查看实际使用的版本

```bash
# 查看依赖树（包含冲突信息）
$ mvn dependency:tree -Dverbose

[INFO] com.example:myapp:jar:1.0.0
[INFO] +- A:A:jar:1.0:compile
[INFO] |  \- com.google.code.gson:gson:jar:2.8.0:compile
[INFO] \- B:B:jar:1.0:compile
[INFO]    \- (com.google.code.gson:gson:jar:2.10.0:compile - omitted for conflict with 2.8.0)
                                                              ↑
                                                            冲突提示
```

---

## 常用 Maven 命令速查

```bash
# 清理编译结果
mvn clean

# 编译主代码
mvn compile

# 运行测试
mvn test

# 打包（jar/war）
mvn package

# 安装到本地仓库
mvn install

# 跳过测试打包（快速）
mvn package -DskipTests

# 查看依赖树
mvn dependency:tree

# 下载源码和文档（IDE 调试用）
mvn dependency:sources
mvn dependency:resolve -Dclassifier=javadoc

# 查看有效 POM（包含继承的配置）
mvn help:effective-pom

# 创建新项目
mvn archetype:generate

# 运行 Spring Boot 应用
mvn spring-boot:run
```

---

## 理解验证

### 问题 1：Maven 坐标

以下 Maven 坐标 `org.springframework.boot:spring-boot-starter-web:3.2.0` 中，哪部分是什么？

<details>
<summary>答案</summary>

- **GroupId**：`org.springframework.boot`（组织/项目）
- **ArtifactId**：`spring-boot-starter-web`（具体的库）
- **Version**：`3.2.0`（版本号）

完整坐标格式：`groupId:artifactId:version`

</details>

### 问题 2：依赖范围

JUnit 测试框架应该用哪个 scope？为什么？

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <version>5.9.0</version>
    <scope>???</scope>
</dependency>
```

<details>
<summary>答案</summary>

**应该用 `test`**

原因：
- JUnit 只在测试代码（src/test/java）中使用
- 业务代码（src/main/java）不需要 JUnit
- 打包时不应该包含 JUnit（生产环境不需要）

如果用 `compile`（默认），会导致：
- 打包的 jar 包含 JUnit（浪费空间）
- 生产代码可以 import JUnit 类（不应该）

</details>

### 问题 3：构建生命周期

运行 `mvn package` 时，Maven 会执行哪些阶段？

<details>
<summary>答案</summary>

**按顺序执行**：
1. validate（验证项目）
2. compile（编译主代码）
3. test（运行测试）
4. package（打包）

**不会执行**：
- clean（需要明确指定：`mvn clean package`）
- install（需要明确指定：`mvn install`）
- deploy（需要明确指定：`mvn deploy`）

生命周期是顺序的：执行某个阶段会自动执行前面的所有阶段。

</details>

### 问题 4：仓库查找顺序

Maven 查找依赖 `com.google.code.gson:gson:2.10.0` 的顺序是什么？

<details>
<summary>答案</summary>

**查找顺序**：
1. **本地仓库**：`~/.m2/repository/com/google/code/gson/gson/2.10.0/`
2. **私有仓库**：如果 pom.xml 或 settings.xml 中配置了
3. **中央仓库**：Maven Central（https://repo.maven.apache.org/maven2/）
4. **下载并缓存**：保存到本地仓库，供下次使用

如果在本地仓库找到，直接使用，不会再去远程查找。

</details>

---

## 总结：Maven 的核心价值

### 三个核心功能

1. **依赖管理**：
   - 声明式依赖（在 pom.xml 中写 GAV 坐标）
   - 自动下载（从中央仓库）
   - 传递依赖（递归下载）
   - 冲突解决（最短路径、第一声明）

2. **标准化构建**：
   - 统一的目录结构（src/main/java）
   - 统一的命令（mvn compile、test、package）
   - 生命周期管理（阶段有序执行）

3. **项目管理**：
   - 项目元数据（groupId、artifactId、version）
   - 多模块支持（父子项目）
   - 插件扩展（自定义构建逻辑）

### Maven vs 手动管理

| 任务 | 手动管理 | Maven |
|------|---------|-------|
| **添加依赖** | 下载 jar，复制到 lib/，配置 classpath | 在 pom.xml 写 3 行 |
| **处理传递依赖** | 手动找所有依赖的依赖 | 自动递归下载 |
| **版本冲突** | 手动测试哪个版本能用 | 自动解决或报告 |
| **构建项目** | 写脚本或用 IDE 按钮 | `mvn package` |
| **团队协作** | 每人配置不同 | 共享 pom.xml |
| **CI/CD** | 为服务器定制脚本 | 所有环境用同样命令 |

### 关键概念速记

- **pom.xml**：项目配置文件（Project Object Model）
- **GAV 坐标**：groupId + artifactId + version（唯一标识一个库）
- **仓库**：本地（~/.m2/repository）+ 中央（Maven Central）+ 私有
- **生命周期**：clean → compile → test → package → install → deploy
- **Scope**：compile（默认）、test（测试）、provided（容器提供）、runtime（运行时）

---

> 完整 Maven 知识树参见 [maven-structure.md](./maven-structure.md)
