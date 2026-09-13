# MVP 团队·前端工程师蒸馏（贾思敏）

> **来源**：WorkBuddy「MVP 开发专家团」子角色「前端工程师·贾思敏」蒸馏（2026-09-06）
> **源包**：`git:mvp-dev-expert-team/agents/mvp-dev-expert-team-frontend.md`（1137 行，核心方法论区已精读）
> **蒸馏方式**：并入 frontend-dev-guide 的 expert-distill。
> **去重说明**：组件分层、工程结构、状态管理、框架选型等已由原生 `前端开发方法论.md` 覆盖；平台代码模板（React/Vue/Next/Taro/Nuxt 五方案结构、小程序 API 替代表、Tailwind 深/浅主题配置）属于**平台落地示例，非方法论**——本文档不重复搬运。
> **只保留增量**：CSS Pro Max 工艺规范（阴影/过渡/色彩/圆角/字距）、强调色配比原则、SEO 实操要点、P0 代码级三禁与扫描命令。

---

## 一、CSS Pro Max 工艺规范（"看不出 AI 做的"代码级关键）

> 前端与设计稿之间的差距，90% 死在这五个细节上。逐条对照改造即可显著去 AI 味。

### 1. 阴影——用光晕代替投影

```css
/* ❌ AI 味：又黑又重的投影 */
.card { box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); }

/* ✅ 浅色主题：柔和阴影（走 Token --elev-raised） */
/* ✅ 深色主题：用 border + 光晕代替投影 */
.card { border: 1px solid var(--border); box-shadow: var(--elev-ring); }
.card:hover { box-shadow: var(--elev-raised); }
```

### 2. 过渡——150ms 是跨系统收敛值

```css
/* ❌ AI 味：0.1s 太生硬 / 0.8s 弹跳缓动 cubic-bezier(0.68,-0.55,0.265,1.55) 太油腻 */
/* ✅ 三档时长：即时反馈 50-100ms · 状态确认 150ms · 进入 UI 200-300ms */
.btn { transition: background-color var(--motion-fast) var(--ease-standard),
                    transform var(--motion-fast) var(--ease-standard),
                    box-shadow var(--motion-fast) var(--ease-standard); }
.btn:hover { transform: translateY(-1px); box-shadow: var(--elev-raised); }

/* 交错动画（列表入场）：逐项 delay 50ms 递增 */
.list-item:nth-child(1) { animation-delay: 0ms; }
.list-item:nth-child(2) { animation-delay: 50ms; }
.list-item:nth-child(3) { animation-delay: 100ms; }
```

### 3. 色彩——永远不用纯黑或纯灰 + 四层调色板

- ❌ `#FFFFFF`/`#000000`/`#808080` 纯色——**永远带色调**（muted 用蓝灰 `#8B949E` 而非纯灰）
- ❌ 到处用强调色——**每屏 ≤2 处强调色使用**
- 四层配比：**中性色 70-90% / 强调色 5-10% / 语义色 0-5% / 效果色 <1%**

### 4. 圆角——有节制 + 四级体系（不过度 round-full）

```
button → var(--radius-sm) 8px  |  card → var(--radius-md) 12px
modal  → var(--radius-lg) 16px |  avatar → var(--radius-pill) 50%
```

### 5. 字距——按场景分级（工艺关键）

```
正文 → 0 ｜ 小字 → 0.01em ｜ ALL CAPS → 必须 0.06em ｜ 标题 32px → -0.01em ｜ 展示 48px → -0.02em
```

---

## 二、P0 代码级三禁（可脚本门禁）

1. **禁 emoji 作功能图标** — 用 Spec 锁定图标库对应语义图标。模块完成即扫：
   ```bash
   grep -rP '[\x{1F300}-\x{1F9FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}]' src/ --include='*.tsx' --include='*.jsx' --include='*.vue' --include='*.html'
   ```
2. **禁硬编码颜色** — 唯一例外 #fff/#000；一律走 Token/Tailwind 语义类
3. **禁 AI 模板代码** — 空洞占位文案、紫粉渐变 class（`from-purple-600 to-pink-500`）一律不写

---

## 三、SEO 实操要点（SSR 方案必做）

| 框架 | 要点 |
|------|------|
| Next.js | Metadata API（title 模板 `%s | 产品名` / description 150 字含关键词 / OpenGraph / Twitter card）+ sitemap.ts + robots.ts + JSON-LD 结构化数据（SoftwareApplication） |
| Nuxt 3 | `useHead`/`useSeoMeta` 逐页设置 |
| SPA（React+Vite） | SEO 天然弱，三选一：react-helmet-async / Prerender.io 预渲染 / 升级 Next.js（推荐长期） |

---

## 四、埋点集成要点（MVP 前端）

- 轻量 SDK + 自建 `track()` 封装（distinctId 用 `crypto.randomUUID()` + localStorage 持久）
- 事件命名 `{对象}_{动作}`；关键事件：注册完成 / 首次核心操作 / 付费点击 / 支付完成 / 错误上报
- **静默失败**：埋点报错不阻塞用户操作

---

## 五、与原生方法论的配合

| 场景 | 用哪个 |
|------|--------|
| 5 场景识别 / 方案产出 / 技术选型 | `前端开发方法论.md`（原生，主） |
| **CSS 工艺细节（阴影/过渡/色彩/圆角/字距）/ SEO / 代码级反 AI 门禁** | **本文档（增量，唯一来源）** |

> **使用原则**：写代码/转设计稿时对照本文档第一节五条工艺规范逐条自查——这五条是"前端产出不像 AI 做的"的最短路径；方案文档阶段仍走原生方法论。

---

_蒸馏记录：v1.0（2026-09-06）· MVP 专家团「前端工程师·贾思敏」→ frontend-dev-guide/expert-distill/_
