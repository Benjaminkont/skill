# 异步编程知识树结构

```
程序执行模式
│
├── 同步执行（Synchronous）
│   └── 阻塞式调用
│
├── 异步执行（Asynchronous）★ 起点
│   ├── 编程模型（如何写）
│   │   ├── Callback（回调函数）
│   │   ├── Promise/Future
│   │   └── async/await
│   │
│   ├── 运行时机制（如何跑）
│   │   ├── Event Loop（事件循环）
│   │   ├── Task Queue（任务队列）
│   │   └── Microtask Queue（微任务队列）
│   │
│   └── 操作系统支持（底层）
│       ├── Non-blocking I/O（非阻塞 I/O）
│       ├── epoll/kqueue（多路复用）
│       └── io_uring（异步 I/O）
│
├── 并行执行（Parallel）
│   ├── 多线程（Multi-threading）
│   ├── 多进程（Multi-processing）
│   └── GPU 并行
│
└── 并发执行（Concurrent）
    ├── 协程（Coroutine）
    └── 绿色线程（Green Thread）
```

## 从"异步"出发的探索路径

**起点**：异步执行（Asynchronous）

**同层兄弟**（同在"程序执行模式"这个房间）：
- 同步执行（Synchronous）
- 并行执行（Parallel）
- 并发执行（Concurrent）

**向上**（谁在使用）：
- Web 应用（浏览器、Node.js）
- 网络服务器（处理大量连接）
- GUI 应用（保持界面响应）

**向下**（内部机制）：
- 编程模型：Callback、Promise、async/await
- 运行时机制：Event Loop、Task Queue
- 操作系统支持：Non-blocking I/O、epoll

**跨系统**：
- 餐厅点餐（号码牌系统）
- 快递配送（异步通知）
