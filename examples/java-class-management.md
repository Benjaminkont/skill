# Java 的类管理：从文件到包的完整机制

## 知识树定位

```
Java（编程语言）
└── 类管理 ★ 起点
    ├── 类的定义与文件
    │   ├── 公共类（public class）- 文件名必须匹配
    │   ├── 包级私有类 - 可多个在一个文件
    │   ├── 内部类（inner class）
    │   └── 匿名类（anonymous class）
    ├── 包管理（package）
    │   ├── 包声明（package 语句）
    │   ├── 包与目录映射
    │   └── 包的访问控制
    └── 类的导入（import）
        ├── 单类导入（import specific）
        ├── 通配符导入（import *）
        └── 静态导入（static import）
```

> 完整知识树参见 [java-structure.md](../knowledge-networks/java-structure.md)

## 直接定义

**Java 的类管理**是 Java 语言规定的"如何将类组织到文件和包中，以及如何在不同类之间建立引用关系"的一套规则。它包括：
- **文件规则**：类与文件的对应关系（public 类必须与文件名一致）
- **包规则**：类如何分组到包中（package 声明 + 目录结构映射）
- **引用规则**：如何使用其他包的类（import 语句）

---

## 同层展开：类的四种定义方式

Java 中的类可以用四种方式定义，它们在**文件分配**上有完全不同的规则。

### 1. 公共类（public class）：一个文件只能有一个

```java
// 文件：User.java
package com.example.model;

public class User {
    private String name;
    private int age;
    
    public User(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

**文件分配规则**：
```
项目根目录/
└── src/
    └── com/
        └── example/
            └── model/
                └── User.java  ← 文件名必须是 User.java
```

**关键约束**：
- ✅ **文件名 = 类名**：`public class User` 必须在 `User.java` 中
- ✅ **目录 = 包路径**：`package com.example.model` 必须在 `com/example/model/` 目录下
- ❌ **一个文件只能有一个 public 类**：不能在 `User.java` 中再定义 `public class Admin`

**如果违反会怎样？**

```java
// 文件：Wrong.java
package com.example.model;

public class User {  // ❌ 编译错误！
    // ...
}
```

**编译器报错**：
```
Error: class User is public, should be declared in a file named User.java
```

---

### 2. 包级私有类：可以多个在同一文件

```java
// 文件：User.java
package com.example.model;

public class User {
    private String name;
    private UserValidator validator;  // 使用包级私有类
    
    public User(String name) {
        this.name = name;
        this.validator = new UserValidator();
    }
    
    public boolean isValid() {
        return validator.validate(this);
    }
}

// 同一个文件中的包级私有类（没有 public 修饰符）
class UserValidator {
    boolean validate(User user) {
        return user.name != null && !user.name.isEmpty();
    }
}

// 还可以再定义一个
class UserHelper {
    static String formatName(String name) {
        return name.trim().toLowerCase();
    }
}
```

**文件分配规则**：
```
src/
└── com/
    └── example/
        └── model/
            └── User.java  ← 包含 3 个类：User(public), UserValidator, UserHelper
```

**关键特性**：
- ✅ **一个文件可以有多个包级私有类**
- ✅ **包级私有类只能被同一个包的类访问**
- ⚠️ **编译后生成多个 .class 文件**：

```
target/classes/
└── com/
    └── example/
        └── model/
            ├── User.class
            ├── UserValidator.class  ← 独立的 .class 文件
            └── UserHelper.class     ← 独立的 .class 文件
```

**什么时候用？**
- 辅助类只被某个公共类使用
- 不希望这个辅助类被其他包看到
- 想减少文件数量（相关的小类放在一起）

---

### 3. 内部类（inner class）：定义在类内部

```java
// 文件：ShoppingCart.java
package com.example.shop;

public class ShoppingCart {
    private List<Item> items = new ArrayList<>();
    
    public void addItem(String product, int quantity, double price) {
        items.add(new Item(product, quantity, price));
    }
    
    public double getTotalPrice() {
        return items.stream()
                    .mapToDouble(Item::getSubtotal)
                    .sum();
    }
    
    // 内部类：购物车项
    private class Item {
        private String product;
        private int quantity;
        private double price;
        
        Item(String product, int quantity, double price) {
            this.product = product;
            this.quantity = quantity;
            this.price = price;
        }
        
        double getSubtotal() {
            return quantity * price;
        }
    }
}
```

**文件分配规则**：
```
源代码：
src/
└── com/
    └── example/
        └── shop/
            └── ShoppingCart.java  ← 只有一个源文件

编译后：
target/classes/
└── com/
    └── example/
        └── shop/
            ├── ShoppingCart.class
            └── ShoppingCart$Item.class  ← 内部类生成 $符号命名的 .class
```

**关键特性**：
- ✅ **内部类可以访问外部类的私有成员**
- ✅ **编译时生成 `外部类$内部类.class`**
- ✅ **逻辑上是一体的，文件管理更清晰**

**静态内部类（static nested class）**：

```java
// 文件：MathUtils.java
package com.example.util;

public class MathUtils {
    
    // 静态内部类：计算结果
    public static class Result {
        private final double value;
        private final String unit;
        
        public Result(double value, String unit) {
            this.value = value;
            this.unit = unit;
        }
        
        public String toString() {
            return value + " " + unit;
        }
    }
    
    public static Result calculateArea(double radius) {
        return new Result(Math.PI * radius * radius, "m²");
    }
}

// 使用方：
// MathUtils.Result result = MathUtils.calculateArea(5.0);
```

**编译后**：
```
target/classes/
└── com/
    └── example/
        └── util/
            ├── MathUtils.class
            └── MathUtils$Result.class  ← 静态内部类
```

**静态 vs 非静态内部类**：
- **非静态内部类**：持有外部类实例的引用，可以访问外部类的实例成员
- **静态内部类**：不持有外部类引用，只能访问外部类的静态成员
- **文件分配**：都在同一个 .java 文件，编译后都生成 `$` 命名的 .class

---

### 4. 匿名类（anonymous class）：临时定义

```java
// 文件：ButtonHandler.java
package com.example.ui;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class ButtonHandler {
    
    public ActionListener createClickHandler(String message) {
        // 匿名类：实现 ActionListener 接口
        return new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                System.out.println("Button clicked: " + message);
            }
        };
    }
    
    public Runnable createTask(int id) {
        // 另一个匿名类：实现 Runnable 接口
        return new Runnable() {
            @Override
            public void run() {
                System.out.println("Task " + id + " running");
            }
        };
    }
}
```

**编译后文件分配**：
```
target/classes/
└── com/
    └── example/
        └── ui/
            ├── ButtonHandler.class
            ├── ButtonHandler$1.class  ← 第一个匿名类（ActionListener）
            └── ButtonHandler$2.class  ← 第二个匿名类（Runnable）
```

**关键特性**：
- ✅ **没有类名**，用 `外部类$数字.class` 命名
- ✅ **适合一次性使用的简单实现**
- ⚠️ **每个匿名类都生成独立的 .class 文件**

**现代替代方案：Lambda 表达式**（Java 8+）：

```java
public class ButtonHandler {
    public ActionListener createClickHandler(String message) {
        // Lambda 表达式：更简洁
        return e -> System.out.println("Button clicked: " + message);
    }
}
```

**编译后**：
```
target/classes/
└── com/
    └── example/
        └── ui/
            └── ButtonHandler.class  ← Lambda 不生成单独的 .class 文件！
```

**Lambda vs 匿名类**：
- Lambda 在运行时通过 `invokedynamic` 字节码动态生成
- 不会产生额外的 .class 文件
- 但只能用于函数式接口（只有一个抽象方法的接口）

---

## 对比表：四种类定义方式的文件分配

| 类型 | 定义位置 | 源文件数量 | .class 文件数量 | 访问范围 | 典型用途 |
|------|---------|-----------|----------------|---------|---------|
| **公共类** | 独立文件 | 1 个 .java | 1 个 .class | 任何包 | 主要的业务类、实体类 |
| **包级私有类** | 与公共类同文件 | 共享 .java | 每个类 1 个 .class | 同一个包 | 辅助类、工具类 |
| **内部类** | 类内部 | 共享 .java | 外部类$内部类.class | 取决于修饰符 | 与外部类紧密关联的类 |
| **匿名类** | 方法内 | 共享 .java | 外部类$数字.class | 仅当前作用域 | 一次性的接口实现 |

---

## 向上抽：包管理系统

现在我们知道了"类如何分配到文件"，但这些文件又是如何组织的？答案是**包（package）**。

### 包的三个作用

#### 作用 1：命名空间（避免类名冲突）

```java
// 文件：src/com/example/util/Date.java
package com.example.util;

public class Date {
    // 你的自定义日期类
}

// 文件：src/com/example/model/Date.java
package com.example.model;

public class Date {
    // 另一个日期类
}
```

**文件分配**：
```
src/
├── com/
│   └── example/
│       ├── util/
│       │   └── Date.java     ← com.example.util.Date
│       └── model/
│           └── Date.java     ← com.example.model.Date
```

**使用时**：
```java
// 文件：src/com/example/Main.java
package com.example;

import com.example.util.Date;  // 导入 util 包的 Date
// import com.example.model.Date;  // 不能同时导入两个 Date

public class Main {
    public static void main(String[] args) {
        Date utilDate = new Date();  // 使用 util.Date
        
        // 如果需要使用 model.Date，必须用全限定名
        com.example.model.Date modelDate = new com.example.model.Date();
    }
}
```

#### 作用 2：访问控制（包级可见性）

```java
// 文件：src/com/example/db/DatabaseConnection.java
package com.example.db;

public class DatabaseConnection {
    private ConnectionPool pool;  // 使用包级私有类
    
    public void connect() {
        pool = ConnectionPool.getInstance();  // ✅ 同包可访问
    }
}

// 同一个文件或同包的另一个文件
class ConnectionPool {  // 包级私有（没有 public）
    private static ConnectionPool instance;
    
    static ConnectionPool getInstance() {
        if (instance == null) {
            instance = new ConnectionPool();
        }
        return instance;
    }
}
```

**文件分配**：
```
src/
└── com/
    └── example/
        └── db/
            ├── DatabaseConnection.java  ← 可以访问 ConnectionPool
            └── ConnectionPool.java      ← 只能被 db 包内的类访问
```

**其他包尝试访问**：
```java
// 文件：src/com/example/service/UserService.java
package com.example.service;

import com.example.db.ConnectionPool;  // ❌ 编译错误！

public class UserService {
    public void process() {
        ConnectionPool pool = ConnectionPool.getInstance();  // ❌ 不可见
    }
}
```

#### 作用 3：逻辑分组（代码组织）

**典型的 Java 项目包结构**：

```
src/
└── com/
    └── mycompany/
        └── myapp/
            ├── model/              ← 实体类（数据模型）
            │   ├── User.java
            │   ├── Product.java
            │   └── Order.java
            ├── repository/         ← 数据访问层
            │   ├── UserRepository.java
            │   └── ProductRepository.java
            ├── service/            ← 业务逻辑层
            │   ├── UserService.java
            │   └── OrderService.java
            ├── controller/         ← 控制器层（Web）
            │   ├── UserController.java
            │   └── ProductController.java
            └── util/               ← 工具类
                ├── DateUtils.java
                └── StringUtils.java
```

**对应的包声明**：
```java
// model/User.java
package com.mycompany.myapp.model;

// service/UserService.java
package com.mycompany.myapp.service;

// controller/UserController.java
package com.mycompany.myapp.controller;
```

---

## 向上抽：Maven 的标准目录结构

实际 Java 项目通常使用构建工具（Maven/Gradle），它们规定了**更严格的目录结构**。

### Maven 标准布局

```
myapp/
├── pom.xml                          ← Maven 配置文件
├── src/
│   ├── main/
│   │   ├── java/                    ← 主代码目录
│   │   │   └── com/
│   │   │       └── mycompany/
│   │   │           └── myapp/
│   │   │               ├── model/
│   │   │               │   └── User.java
│   │   │               ├── service/
│   │   │               │   └── UserService.java
│   │   │               └── Main.java
│   │   ├── resources/               ← 资源文件（配置、模板等）
│   │   │   ├── application.properties
│   │   │   └── logback.xml
│   │   └── webapp/                  ← Web 资源（HTML、CSS、JS）
│   │       └── WEB-INF/
│   │           └── web.xml
│   └── test/
│       ├── java/                    ← 测试代码目录
│       │   └── com/
│       │       └── mycompany/
│       │           └── myapp/
│       │               └── service/
│       │                   └── UserServiceTest.java
│       └── resources/               ← 测试资源
│           └── test-data.sql
└── target/                          ← 编译输出目录（Maven 自动生成）
    ├── classes/                     ← 编译后的主代码
    │   └── com/
    │       └── mycompany/
    │           └── myapp/
    │               ├── model/
    │               │   └── User.class
    │               └── service/
    │                   └── UserService.class
    ├── test-classes/                ← 编译后的测试代码
    └── myapp-1.0.jar                ← 最终打包的 JAR 文件
```

**关键约定**：
- ✅ **src/main/java**：所有生产代码必须在这里
- ✅ **src/test/java**：所有测试代码必须在这里
- ✅ **包路径 = 目录路径**：`com.mycompany.myapp.model.User` 必须在 `src/main/java/com/mycompany/myapp/model/User.java`
- ✅ **target/ 是生成目录**：不要手动修改，每次构建会清空

---

## 向下插：import 的三种方式

现在我们知道了类如何组织到包中，那如何**引用其他包的类**？

### 方式 1：单类导入（推荐）

```java
// 文件：src/com/example/service/UserService.java
package com.example.service;

import com.example.model.User;          // 导入单个类
import com.example.repository.UserRepository;
import java.util.List;
import java.util.ArrayList;

public class UserService {
    private UserRepository repository;
    
    public List<User> getAllUsers() {
        return repository.findAll();
    }
}
```

**优点**：
- ✅ 明确显示使用了哪些类
- ✅ IDE 可以自动优化导入
- ✅ 避免命名冲突

### 方式 2：通配符导入（谨慎使用）

```java
package com.example.service;

import com.example.model.*;      // 导入 model 包的所有类
import java.util.*;               // 导入 util 包的所有类

public class UserService {
    private User user;            // 来自 com.example.model.User
    private List<String> names;   // 来自 java.util.List
}
```

**问题场景**：
```java
import java.util.*;
import java.sql.*;

public class Example {
    public void process() {
        Date date = new Date();  // ❌ 编译错误！
        // 编译器不知道是 java.util.Date 还是 java.sql.Date
    }
}
```

**解决方案**：
```java
import java.util.*;
import java.sql.*;

public class Example {
    public void process() {
        java.util.Date utilDate = new java.util.Date();  // 用全限定名
        java.sql.Date sqlDate = new java.sql.Date(System.currentTimeMillis());
    }
}
```

### 方式 3：静态导入（导入静态成员）

```java
// 普通导入
import java.lang.Math;

public class Calculator {
    public double calculate(double x) {
        return Math.sqrt(Math.pow(x, 2) + Math.PI);  // 需要写 Math.
    }
}

// 静态导入
import static java.lang.Math.*;  // 导入 Math 的所有静态成员

public class Calculator {
    public double calculate(double x) {
        return sqrt(pow(x, 2) + PI);  // 直接用静态方法和常量
    }
}
```

**静态导入的实际例子**：

```java
// 测试代码中常见
import static org.junit.Assert.*;  // 导入所有断言方法

public class UserTest {
    @Test
    public void testUserCreation() {
        User user = new User("Alice", 25);
        
        // 直接用断言方法，不用写 Assert.
        assertEquals("Alice", user.getName());
        assertTrue(user.getAge() > 0);
        assertNotNull(user);
    }
}
```

**何时使用静态导入**：
- ✅ 测试代码（断言方法）
- ✅ 常量定义（如 `TimeUnit.SECONDS`）
- ✅ 工具方法（如 `Collections.emptyList()`）
- ❌ 避免滥用：会降低代码可读性（看不出方法来自哪里）

---

## 实战案例：完整的电商系统文件布局

### 场景描述

我们要构建一个小型电商系统，包括：
- 用户管理
- 商品管理
- 订单处理

### 完整的文件结构

```
ecommerce/
├── pom.xml
└── src/
    └── main/
        └── java/
            └── com/
                └── shop/
                    ├── model/                           ← 实体类
                    │   ├── User.java
                    │   ├── Product.java
                    │   ├── Order.java
                    │   └── OrderItem.java               ← Order 的明细项
                    ├── repository/                      ← 数据访问
                    │   ├── UserRepository.java
                    │   ├── ProductRepository.java
                    │   └── OrderRepository.java
                    ├── service/                         ← 业务逻辑
                    │   ├── UserService.java
                    │   ├── ProductService.java
                    │   └── OrderService.java
                    ├── dto/                             ← 数据传输对象
                    │   ├── CreateOrderRequest.java
                    │   └── OrderSummary.java
                    ├── exception/                       ← 自定义异常
                    │   ├── UserNotFoundException.java
                    │   └── InsufficientStockException.java
                    └── util/                            ← 工具类
                        ├── PriceCalculator.java
                        └── DateFormatter.java
```

### 具体代码示例

#### 1. 实体类（model 包）

```java
// 文件：src/main/java/com/shop/model/Order.java
package com.shop.model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class Order {
    private Long id;
    private User user;
    private LocalDateTime createdAt;
    private List<OrderItem> items;
    private OrderStatus status;
    
    // 内部枚举：订单状态
    public enum OrderStatus {
        PENDING,
        PAID,
        SHIPPED,
        COMPLETED,
        CANCELLED
    }
    
    public Order(User user) {
        this.user = user;
        this.createdAt = LocalDateTime.now();
        this.items = new ArrayList<>();
        this.status = OrderStatus.PENDING;
    }
    
    public void addItem(Product product, int quantity) {
        items.add(new OrderItem(product, quantity));
    }
    
    public double getTotalPrice() {
        return items.stream()
                    .mapToDouble(OrderItem::getSubtotal)
                    .sum();
    }
    
    // 内部类：订单明细项（紧密关联，不需要单独文件）
    public static class OrderItem {
        private Product product;
        private int quantity;
        
        public OrderItem(Product product, int quantity) {
            this.product = product;
            this.quantity = quantity;
        }
        
        public double getSubtotal() {
            return product.getPrice() * quantity;
        }
        
        public Product getProduct() {
            return product;
        }
        
        public int getQuantity() {
            return quantity;
        }
    }
    
    // Getters and setters...
}
```

**编译后的文件**：
```
target/classes/com/shop/model/
├── Order.class
├── Order$OrderStatus.class      ← 枚举生成独立 .class
└── Order$OrderItem.class        ← 内部类生成独立 .class
```

#### 2. 数据访问层（repository 包）

```java
// 文件：src/main/java/com/shop/repository/OrderRepository.java
package com.shop.repository;

import com.shop.model.Order;
import com.shop.model.User;
import java.util.List;
import java.util.Optional;

public interface OrderRepository {
    Order save(Order order);
    Optional<Order> findById(Long id);
    List<Order> findByUser(User user);
    List<Order> findAll();
}

// 实现类（可以在同一个文件中，包级私有）
class OrderRepositoryImpl implements OrderRepository {
    // 简化示例：用内存存储
    private final Map<Long, Order> storage = new HashMap<>();
    private Long nextId = 1L;
    
    @Override
    public Order save(Order order) {
        if (order.getId() == null) {
            order.setId(nextId++);
        }
        storage.put(order.getId(), order);
        return order;
    }
    
    @Override
    public Optional<Order> findById(Long id) {
        return Optional.ofNullable(storage.get(id));
    }
    
    @Override
    public List<Order> findByUser(User user) {
        return storage.values().stream()
                      .filter(order -> order.getUser().equals(user))
                      .collect(Collectors.toList());
    }
    
    @Override
    public List<Order> findAll() {
        return new ArrayList<>(storage.values());
    }
}
```

**文件布局**：
```
src/main/java/com/shop/repository/
└── OrderRepository.java    ← 包含接口和实现类

编译后：
target/classes/com/shop/repository/
├── OrderRepository.class
└── OrderRepositoryImpl.class    ← 实现类独立的 .class
```

**为什么不把实现类分开文件？**
- 实现类是包级私有，只在包内使用
- 接口和实现逻辑紧密关联
- 减少文件数量，方便维护

#### 3. 业务逻辑层（service 包）

```java
// 文件：src/main/java/com/shop/service/OrderService.java
package com.shop.service;

import com.shop.model.Order;
import com.shop.model.Product;
import com.shop.model.User;
import com.shop.repository.OrderRepository;
import com.shop.repository.ProductRepository;
import com.shop.exception.InsufficientStockException;
import com.shop.dto.CreateOrderRequest;
import com.shop.util.PriceCalculator;

import java.util.List;

public class OrderService {
    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;
    private final PriceCalculator priceCalculator;
    
    public OrderService(OrderRepository orderRepository,
                       ProductRepository productRepository) {
        this.orderRepository = orderRepository;
        this.productRepository = productRepository;
        this.priceCalculator = new PriceCalculator();
    }
    
    public Order createOrder(User user, CreateOrderRequest request) {
        Order order = new Order(user);
        
        // 使用匿名类处理每个订单项
        request.getItems().forEach(item -> {
            Product product = productRepository.findById(item.getProductId())
                    .orElseThrow(() -> new IllegalArgumentException("Product not found"));
            
            if (product.getStock() < item.getQuantity()) {
                throw new InsufficientStockException(
                        "Insufficient stock for product: " + product.getName());
            }
            
            order.addItem(product, item.getQuantity());
            
            // 减少库存
            product.setStock(product.getStock() - item.getQuantity());
            productRepository.save(product);
        });
        
        return orderRepository.save(order);
    }
    
    public List<Order> getUserOrders(User user) {
        return orderRepository.findByUser(user);
    }
    
    public double calculateOrderTotal(Order order) {
        return priceCalculator.calculate(order);
    }
}
```

**导入语句分析**：
```java
// 模型类（同项目）
import com.shop.model.Order;
import com.shop.model.Product;
import com.shop.model.User;

// 数据访问层（同项目）
import com.shop.repository.OrderRepository;
import com.shop.repository.ProductRepository;

// 异常类（同项目）
import com.shop.exception.InsufficientStockException;

// DTO（同项目）
import com.shop.dto.CreateOrderRequest;

// 工具类（同项目）
import com.shop.util.PriceCalculator;

// JDK 标准库
import java.util.List;
```

#### 4. DTO（数据传输对象）

```java
// 文件：src/main/java/com/shop/dto/CreateOrderRequest.java
package com.shop.dto;

import java.util.List;

public class CreateOrderRequest {
    private Long userId;
    private List<OrderItemRequest> items;
    
    // 静态内部类：订单项请求（DTO 的一部分）
    public static class OrderItemRequest {
        private Long productId;
        private int quantity;
        
        public OrderItemRequest() {}
        
        public OrderItemRequest(Long productId, int quantity) {
            this.productId = productId;
            this.quantity = quantity;
        }
        
        public Long getProductId() { return productId; }
        public int getQuantity() { return quantity; }
        
        public void setProductId(Long productId) { this.productId = productId; }
        public void setQuantity(int quantity) { this.quantity = quantity; }
    }
    
    // Getters and setters...
    public Long getUserId() { return userId; }
    public List<OrderItemRequest> getItems() { return items; }
    
    public void setUserId(Long userId) { this.userId = userId; }
    public void setItems(List<OrderItemRequest> items) { this.items = items; }
}
```

**使用示例**：
```java
// 创建订单请求
CreateOrderRequest request = new CreateOrderRequest();
request.setUserId(1L);

List<CreateOrderRequest.OrderItemRequest> items = Arrays.asList(
    new CreateOrderRequest.OrderItemRequest(101L, 2),  // 商品 101，数量 2
    new CreateOrderRequest.OrderItemRequest(102L, 1)   // 商品 102，数量 1
);
request.setItems(items);

Order order = orderService.createOrder(user, request);
```

**编译后**：
```
target/classes/com/shop/dto/
├── CreateOrderRequest.class
└── CreateOrderRequest$OrderItemRequest.class  ← 静态内部类
```

---

## 理解验证

请回答以下问题，检查你的理解：

### 问题 1：文件命名

假设你在 `src/main/java/com/shop/service/` 目录下，想创建一个订单服务类。以下哪些是合法的？

A. 文件名：`OrderService.java`，类名：`public class OrderService`  
B. 文件名：`OrderHandler.java`，类名：`public class OrderService`  
C. 文件名：`OrderService.java`，包含两个类：`public class OrderService` 和 `public class OrderHelper`  
D. 文件名：`OrderService.java`，包含两个类：`public class OrderService` 和 `class OrderValidator`

<details>
<summary>答案</summary>

- **A：✅ 正确**：文件名与公共类名一致
- **B：❌ 错误**：public 类 `OrderService` 必须在 `OrderService.java` 中
- **C：❌ 错误**：一个文件只能有一个 public 类
- **D：✅ 正确**：可以有一个 public 类 + 多个包级私有类

</details>

### 问题 2：编译后的文件

下面的代码编译后会生成几个 .class 文件？

```java
// 文件：Calculator.java
package com.util;

public class Calculator {
    public static class Result {
        private double value;
    }
    
    public Result calculate(int x) {
        return new Result();
    }
    
    public Comparator<Result> getComparator() {
        return new Comparator<Result>() {
            public int compare(Result r1, Result r2) {
                return Double.compare(r1.value, r2.value);
            }
        };
    }
}
```

A. 1 个  
B. 2 个  
C. 3 个  
D. 4 个

<details>
<summary>答案</summary>

**C：3 个**

1. `Calculator.class` - 外部类
2. `Calculator$Result.class` - 静态内部类
3. `Calculator$1.class` - 匿名类（Comparator 实现）

</details>

### 问题 3：包和目录

以下代码的正确文件路径是什么？

```java
package com.mycompany.shop.service;

public class UserService {
    // ...
}
```

假设项目根目录是 `/home/user/myproject`，使用 Maven 标准布局。

<details>
<summary>答案</summary>

**正确路径**：
```
/home/user/myproject/src/main/java/com/mycompany/shop/service/UserService.java
```

**关键点**：
- Maven 主代码在 `src/main/java/` 下
- 包路径 `com.mycompany.shop.service` 映射到目录 `com/mycompany/shop/service/`
- 文件名必须是 `UserService.java`（与类名一致）

</details>

### 问题 4：导入冲突

以下代码有什么问题？如何修复？

```java
package com.shop.util;

import java.util.*;
import java.sql.*;

public class DateUtils {
    public void process() {
        Date now = new Date();  // ❓ 这是哪个 Date？
    }
}
```

<details>
<summary>答案</summary>

**问题**：`Date` 类在 `java.util` 和 `java.sql` 中都存在，编译器无法确定使用哪个。

**修复方案 1**：使用全限定名
```java
public void process() {
    java.util.Date now = new java.util.Date();
}
```

**修复方案 2**：改用单类导入
```java
import java.util.Date;  // 明确导入 util.Date
import java.sql.Timestamp;  // 只导入需要的 sql 类

public class DateUtils {
    public void process() {
        Date now = new Date();  // ✅ 明确是 util.Date
    }
}
```

**修复方案 3**：使用 Java 8+ 的新日期 API（最佳实践）
```java
import java.time.LocalDateTime;

public class DateUtils {
    public void process() {
        LocalDateTime now = LocalDateTime.now();  // ✅ 无冲突
    }
}
```

</details>

---

## 总结：Java 类管理的核心规则

### 文件分配规则

| 规则 | 说明 | 示例 |
|-----|------|-----|
| **公共类 = 文件名** | public class 必须与文件名一致 | `User.java` 包含 `public class User` |
| **目录 = 包路径** | 包路径必须与目录结构一致 | `package com.shop.model` → `com/shop/model/` |
| **一文件一公共类** | 一个 .java 只能有一个 public 类 | ✅ 一个 public + 多个包级私有 |
| **内部类 = $ 命名** | 内部类编译成 `外部$内部.class` | `Order$OrderItem.class` |
| **匿名类 = $数字** | 匿名类编译成 `外部$数字.class` | `Handler$1.class` |

### 包管理规则

1. **命名空间**：避免类名冲突
2. **访问控制**：包级私有类只能被同包访问
3. **逻辑分组**：按功能组织代码（model、service、repository 等）

### Maven 标准布局

```
src/
├── main/java/      ← 生产代码
├── main/resources/ ← 配置文件
├── test/java/      ← 测试代码
└── test/resources/ ← 测试资源

target/             ← 编译输出（自动生成）
```

### 最佳实践

✅ **推荐**：
- 每个公共类独立文件
- 辅助类用包级私有，与主类放在同一文件
- 紧密关联的类用内部类
- 单类导入，避免通配符
- 遵循 Maven 标准布局

❌ **避免**：
- 文件名与类名不一致
- 包路径与目录不一致
- 滥用通配符导入（`import *`）
- 把所有类都做成 public
- 在 target/ 目录手动修改文件

---

> 完整 Java 知识树参见 [java-structure.md](../knowledge-networks/java-structure.md)
