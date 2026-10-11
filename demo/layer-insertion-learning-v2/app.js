// 知识图谱数据结构
const knowledgeGraph = {
  'docker-container': {
    icon: '🐳',
    title: 'Docker 容器',
    definition: '轻量级、可移植的应用运行环境',
    horizontal: [
      {
        id: 'vm',
        icon: '💻',
        title: '虚拟机',
        desc: '完整的操作系统虚拟化',
        relation: '都提供隔离环境，但容器更轻量、启动更快'
      },
      {
        id: 'process',
        icon: '⚙️',
        title: '进程',
        desc: '操作系统中的执行单元',
        relation: '容器本质是特殊的进程组，但有独立的文件系统和网络'
      },
      {
        id: 'lxc',
        icon: '📦',
        title: 'LXC',
        desc: 'Linux 容器技术',
        relation: 'Docker 早期基于 LXC，现在有自己的容器运行时'
      }
    ],
    up: [
      {
        id: 'kubernetes',
        icon: '☸️',
        title: 'Kubernetes',
        desc: '容器编排平台',
        relation: 'K8s 调度和管理大量容器，容器是它的基本单元'
      },
      {
        id: 'docker-compose',
        icon: '🎼',
        title: 'Docker Compose',
        desc: '多容器应用定义工具',
        relation: '用 YAML 定义多个容器如何协作'
      }
    ],
    cross: [
      {
        id: 'shipping-container',
        icon: '🚢',
        title: '货运集装箱',
        desc: '标准化的货物运输单元',
        relation: '都解决了"标准化打包"问题，但集装箱是物理空间，容器是进程隔离',
        warning: '⚠️ 只是概念类比，实现机制完全不同'
      }
    ],
    down: [
      {
        id: 'namespace',
        icon: '🔒',
        title: 'Namespace',
        desc: 'Linux 内核隔离机制',
        relation: '提供 PID、网络、文件系统等多个维度的隔离'
      },
      {
        id: 'cgroup',
        icon: '📊',
        title: 'Cgroup',
        desc: '资源限制和监控',
        relation: '限制容器可使用的 CPU、内存等资源'
      },
      {
        id: 'union-fs',
        icon: '🗂️',
        title: 'Union FS',
        desc: '联合文件系统',
        relation: '分层镜像的基础，实现增量存储'
      }
    ],
    insight: {
      horizontal: '通过对比虚拟机、进程、LXC，我们明确了容器的定位：比虚拟机轻量，比普通进程隔离性更强。',
      up: '理解了 Kubernetes 和 Docker Compose 如何使用容器，就明白了容器为什么要设计成"无状态"和"可替换"的。',
      cross: '货运集装箱的类比帮助理解"标准化打包"的价值，但要记住这只是概念相似——容器不是物理隔离，而是通过内核特性实现的逻辑隔离。',
      down: '深入 namespace、cgroup 和 UnionFS，才能理解容器"轻量"和"快速"的原因：它不是虚拟化硬件，而是复用内核、隔离资源。'
    }
  },
  'kubernetes': {
    icon: '☸️',
    title: 'Kubernetes',
    definition: '自动化容器编排、部署和管理平台',
    horizontal: [
      {
        id: 'docker-swarm',
        icon: '🐝',
        title: 'Docker Swarm',
        desc: 'Docker 原生编排工具',
        relation: '都做容器编排，K8s 功能更强大但复杂度更高'
      },
      {
        id: 'nomad',
        icon: '🎯',
        title: 'Nomad',
        desc: 'HashiCorp 的编排工具',
        relation: '更简单，但生态不如 K8s 丰富'
      }
    ],
    up: [
      {
        id: 'platform',
        icon: '🏗️',
        title: '云原生平台',
        desc: '完整的应用平台',
        relation: 'K8s 是云原生平台的核心调度层'
      }
    ],
    cross: [
      {
        id: 'orchestra',
        icon: '🎻',
        title: '交响乐团指挥',
        desc: '协调众多乐手演奏',
        relation: 'K8s 像指挥家协调容器，但指挥只能指导人，K8s 能自动重启失败的容器',
        warning: '⚠️ 类比有助于理解协调作用，但 K8s 的自愈能力是指挥不具备的'
      }
    ],
    down: [
      {
        id: 'pod',
        icon: '🫘',
        title: 'Pod',
        desc: 'K8s 最小调度单元',
        relation: 'Pod 包含一个或多个容器，共享网络和存储'
      },
      {
        id: 'scheduler',
        icon: '📅',
        title: 'Scheduler',
        desc: 'Pod 调度器',
        relation: '决定 Pod 应该运行在哪个节点上'
      }
    ],
    insight: {
      horizontal: '对比其他编排工具，理解 K8s 的优势：强大的声明式 API、丰富的生态、大规模实战验证。',
      up: '理解云原生平台如何使用 K8s，就明白了为什么 K8s 要设计得如此灵活和可扩展。',
      cross: '指挥家的类比帮助理解"协调"的概念，但 K8s 的自愈、自动扩缩容能力超越了简单的协调。',
      down: '深入 Pod、Scheduler 等组件，理解 K8s 如何将"期望状态"变成"实际状态"。'
    }
  },
  'namespace': {
    icon: '🔒',
    title: 'Namespace',
    definition: 'Linux 内核的资源隔离机制',
    horizontal: [
      {
        id: 'cgroup',
        icon: '📊',
        title: 'Cgroup',
        desc: '资源限制机制',
        relation: '都是容器隔离的基础，namespace 隔离视野，cgroup 限制资源'
      },
      {
        id: 'selinux',
        icon: '🛡️',
        title: 'SELinux',
        desc: '安全增强模块',
        relation: '提供更细粒度的访问控制'
      }
    ],
    up: [
      {
        id: 'docker-container',
        icon: '🐳',
        title: 'Docker 容器',
        desc: '容器运行时',
        relation: '容器通过 namespace 实现隔离'
      }
    ],
    cross: [
      {
        id: 'apartment',
        icon: '🏢',
        title: '公寓隔间',
        desc: '同一建筑内的独立空间',
        relation: '都是在共享基础上创建独立空间，但公寓是物理墙，namespace 是内核视图隔离',
        warning: '⚠️ 类比有助理解"共享内核但隔离视图"，但 namespace 不是物理隔离'
      }
    ],
    down: [
      {
        id: 'pid-namespace',
        icon: '🆔',
        title: 'PID Namespace',
        desc: '进程 ID 隔离',
        relation: '每个容器有独立的进程树'
      },
      {
        id: 'net-namespace',
        icon: '🌐',
        title: 'Net Namespace',
        desc: '网络栈隔离',
        relation: '独立的 IP、端口、路由表'
      },
      {
        id: 'mount-namespace',
        icon: '📁',
        title: 'Mount Namespace',
        desc: '文件系统挂载点隔离',
        relation: '每个容器看到不同的文件系统视图'
      }
    ],
    insight: {
      horizontal: '对比 cgroup 和 SELinux，理解 namespace 专注于"视图隔离"而非资源限制或安全策略。',
      up: '理解容器如何使用 namespace，就明白了为什么容器启动快、占用少——它们共享内核。',
      cross: '公寓隔间的类比帮助理解"共享基础设施但彼此独立"，但要记住这是逻辑隔离，不是物理隔离。',
      down: '深入 PID、Net、Mount 等具体 namespace，看到内核如何在多个维度实现隔离。'
    }
  }
};

// 状态管理
let currentConcept = 'docker-container';
let explorationPath = ['docker-container'];
let activeZone = null;

// 粒子系统
class ParticleSystem {
  constructor(canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.particles = [];
    this.resize();
    this.init();
    window.addEventListener('resize', () => this.resize());
  }

  resize() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  init() {
    for (let i = 0; i < 80; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        size: Math.random() * 2 + 0.5
      });
    }
    this.animate();
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    this.particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;

      this.ctx.fillStyle = 'rgba(0, 217, 255, 0.4)';
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      this.ctx.fill();
    });

    // 绘制连线
    this.ctx.strokeStyle = 'rgba(0, 217, 255, 0.1)';
    this.ctx.lineWidth = 0.5;
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const dx = this.particles[i].x - this.particles[j].x;
        const dy = this.particles[i].y - this.particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < 120) {
          this.ctx.beginPath();
          this.ctx.moveTo(this.particles[i].x, this.particles[i].y);
          this.ctx.lineTo(this.particles[j].x, this.particles[j].y);
          this.ctx.stroke();
        }
      }
    }

    requestAnimationFrame(() => this.animate());
  }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  const canvas = document.getElementById('particles');
  new ParticleSystem(canvas);

  renderCenterNode(currentConcept);
  updatePathTracker();
  setupZoneTriggers();
  setupControls();
});

// 渲染中心节点
function renderCenterNode(conceptId) {
  const concept = knowledgeGraph[conceptId];
  const centerNode = document.getElementById('centerNode');

  centerNode.innerHTML = `
    <div class="node-glow"></div>
    <div class="node-core">
      <div class="node-icon">${concept.icon}</div>
      <h2 class="node-title">${concept.title}</h2>
      <p class="node-definition">${concept.definition}</p>
    </div>
    <div class="pulse-ring"></div>
  `;

  // 添加点击事件
  centerNode.querySelector('.node-core').addEventListener('click', () => {
    showInsight(conceptId, 'center');
  });
}

// 设置区域触发器
function setupZoneTriggers() {
  const triggers = document.querySelectorAll('.zone-trigger');

  triggers.forEach(trigger => {
    trigger.addEventListener('click', () => {
      const direction = trigger.dataset.direction;
      toggleZone(direction);
    });
  });
}

// 切换区域
function toggleZone(direction) {
  const zone = document.querySelector(`.zone-${direction}`);
  const content = zone.querySelector('.zone-content');
  const trigger = zone.querySelector('.zone-trigger');

  // 关闭其他区域
  document.querySelectorAll('.zone-content').forEach(c => {
    if (c !== content) {
      c.classList.remove('visible');
      c.innerHTML = '';
    }
  });

  document.querySelectorAll('.zone-trigger').forEach(t => {
    if (t !== trigger) {
      t.classList.remove('active');
    }
  });

  if (content.classList.contains('visible')) {
    content.classList.remove('visible');
    trigger.classList.remove('active');
    activeZone = null;
    setTimeout(() => content.innerHTML = '', 600);
  } else {
    content.classList.add('visible');
    trigger.classList.add('active');
    activeZone = direction;
    renderZoneContent(direction, content);
  }
}

// 渲染区域内容
function renderZoneContent(direction, container) {
  const concept = knowledgeGraph[currentConcept];
  const items = concept[direction] || [];

  container.innerHTML = '';

  items.forEach((item, index) => {
    const card = document.createElement('div');
    card.className = 'concept-card';
    card.style.animationDelay = `${index * 0.1}s`;
    card.innerHTML = `
      <div class="concept-icon">${item.icon}</div>
      <div class="concept-title">${item.title}</div>
      <div class="concept-desc">${item.desc}</div>
      <div class="concept-relation">${item.relation}</div>
    `;

    card.addEventListener('click', () => {
      if (knowledgeGraph[item.id]) {
        navigateToConcept(item.id);
      } else {
        showInsight(currentConcept, direction, item);
      }
    });

    container.appendChild(card);
  });
}

// 导航到新概念
function navigateToConcept(conceptId) {
  currentConcept = conceptId;
  explorationPath.push(conceptId);

  // 关闭所有区域
  document.querySelectorAll('.zone-content').forEach(c => {
    c.classList.remove('visible');
    c.innerHTML = '';
  });

  document.querySelectorAll('.zone-trigger').forEach(t => {
    t.classList.remove('active');
  });

  activeZone = null;

  // 更新中心节点
  renderCenterNode(conceptId);
  updatePathTracker();

  // 显示洞察
  showInsight(conceptId, 'center');
}

// 显示洞察面板
function showInsight(conceptId, direction, item = null) {
  const concept = knowledgeGraph[conceptId];
  const panel = document.getElementById('insightPanel');
  const content = document.getElementById('insightContent');

  let html = `<h4>💡 理解要点</h4>`;

  if (direction === 'center') {
    html += `<p>${concept.definition}</p>`;
    html += `<div class="insight-highlight">
      现在你可以探索四个方向：<br>
      • <strong>同层对照</strong>：看看相似的概念<br>
      • <strong>向上抽取</strong>：谁在使用它<br>
      • <strong>跨系统类比</strong>：其他领域的相似物<br>
      • <strong>向下深入</strong>：它如何实现
    </div>`;
  } else if (concept.insight && concept.insight[direction]) {
    html += `<p>${concept.insight[direction]}</p>`;

    if (item && item.warning) {
      html += `<div class="insight-highlight" style="border-color: #ffb86c;">
        ${item.warning}
      </div>`;
    }
  }

  content.innerHTML = html;
  panel.classList.add('visible');
}

// 更新路径追踪
function updatePathTracker() {
  const pathItems = document.getElementById('pathItems');
  pathItems.innerHTML = '';

  explorationPath.forEach((conceptId, index) => {
    const concept = knowledgeGraph[conceptId];

    if (index > 0) {
      const arrow = document.createElement('span');
      arrow.className = 'path-arrow';
      arrow.textContent = '→';
      pathItems.appendChild(arrow);
    }

    const item = document.createElement('div');
    item.className = 'path-item';
    item.innerHTML = `<span>${concept.icon}</span><span>${concept.title}</span>`;

    item.addEventListener('click', () => {
      if (index < explorationPath.length - 1) {
        explorationPath = explorationPath.slice(0, index + 1);
        currentConcept = conceptId;
        renderCenterNode(conceptId);
        updatePathTracker();

        // 关闭区域
        document.querySelectorAll('.zone-content').forEach(c => {
          c.classList.remove('visible');
          c.innerHTML = '';
        });
        document.querySelectorAll('.zone-trigger').forEach(t => {
          t.classList.remove('active');
        });
      }
    });

    pathItems.appendChild(item);
  });
}

// 设置控制按钮
function setupControls() {
  document.getElementById('reset').addEventListener('click', () => {
    currentConcept = 'docker-container';
    explorationPath = ['docker-container'];
    renderCenterNode(currentConcept);
    updatePathTracker();

    document.querySelectorAll('.zone-content').forEach(c => {
      c.classList.remove('visible');
      c.innerHTML = '';
    });
    document.querySelectorAll('.zone-trigger').forEach(t => {
      t.classList.remove('active');
    });

    document.getElementById('insightPanel').classList.remove('visible');
  });

  document.getElementById('closeInsight').addEventListener('click', () => {
    document.getElementById('insightPanel').classList.remove('visible');
  });

  document.getElementById('history').addEventListener('click', () => {
    alert('探索历史：\n\n' + explorationPath.map((id, i) => {
      const c = knowledgeGraph[id];
      return `${i + 1}. ${c.icon} ${c.title}`;
    }).join('\n'));
  });
}
