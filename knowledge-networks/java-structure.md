# Java 知识网络

范围为 Java 语言内的类型、名称、包、类管理与编译运行。跨语言比较见 [代码文件管理](code-file-management-structure.md)，构建和依赖细节见 [Maven](maven-structure.md)。

```
Java（编程语言）
│
├── 类型系统
│   ├── 基本类型（int, boolean, etc.）
│   ├── 引用类型
│   │   ├── 类（class）
│   │   ├── 接口（interface）
│   │   ├── 枚举（enum）
│   │   └── 注解（annotation）
│   └── 数组类型
│
├── 类管理
│   ├── 类的定义与文件
│   │   ├── 公共类（public class）- 文件名必须匹配
│   │   ├── 包级私有类 - 可多个在一个文件
│   │   ├── 内部类（inner class）
│   │   └── 匿名类（anonymous class）
│   ├── 包管理（package）
│   │   ├── 包声明（package 语句）
│   │   ├── 包与目录映射
│   │   └── 包的访问控制
│   ├── 类的导入（import）
│   │   ├── 单类导入（import specific）
│   │   ├── 通配符导入（import *）
│   │   └── 静态导入（static import）
│   └── 类的访问控制
│       ├── public（公共访问）
│       ├── protected（受保护访问）
│       ├── package-private（包私有，默认）
│       └── private（私有访问）
│
├── 编译与运行
│   ├── 源代码编译（.java → .class）
│   ├── 字节码结构（.class 文件）
│   ├── 类加载器（ClassLoader）
│   └── JVM 运行时
│
└── 构建工具
    ├── Maven（约定式目录结构）
    ├── Gradle
    └── IDE 项目结构
```
