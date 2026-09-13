# 前端开发专家蒸馏 · Frontend Developer（像素匠）

> **来源**：WorkBuddy 专家中心「像素匠·前端开发」专家包蒸馏（2026-09-06）
> **源包**：`~/.workbuddy/plugins/marketplaces/experts/plugins/frontend-developer/agents/frontend-developer.md`（235 行）
> **蒸馏方式**：并入 frontend-dev-guide 的 expert-distill。
> **去重说明**：组件分层/技术选型已由原生方法论覆盖，CSS 工艺细节已由 mvp-frontend 蒸馏（贾思敏）覆盖；本文档**只保留增量**——性能量化基线（Core Web Vitals）、大数据表格虚拟化模式、前端交付模板（UI/性能/无障碍三节）、无障碍自动化进 CI。

---

## 一、前端成功指标（量化基线，目标可验收）

| 指标 | 目标 |
|------|------|
| Core Web Vitals | LCP < 2.5s / FID < 100ms / CLS < 0.1 |
| 慢网加载 | 3G 网络下 < 3 秒 |
| Lighthouse | Performance + Accessibility 均 > 90 |
| 组件复用率 | > 80% |
| 生产环境 | 零 console error |

**性能优先纪律**：CWV 从项目开始就优化（不是上线前补）；图片 WebP/AVIF + 响应式 srcset；代码分割 + 懒加载；Service Worker + CDN 缓存；Real User Monitoring（RUM）追踪真实性能。

---

## 二、大数据表格虚拟化模式（性能关键路径）

> 渲染千行数据表 = 前端性能头号杀手。用虚拟化 + memo 三件套：

```tsx
// @tanstack/react-virtual 虚拟滚动 + memo/useCallback/useMemo 防重渲
const rowVirtualizer = useVirtualizer({
  count: data.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 50,
  overscan: 5,                    // 预渲染窗口
});
// 表格语义：容器 role="table" aria-label，行 role="row" tabIndex={0}，单元格 role="cell"
// 行点击用 useCallback 包裹；组件整体 export const X = memo<Props>(...)
```

**要点**：列表/表格数据量可能上千时，第一版就用虚拟化——后期替换成本远高于一开始就用。

---

## 三、前端交付模板（UI / 性能 / 无障碍三节）

```markdown
# [项目名] 前端实现

## UI 实现
**框架**：[React/Vue 含版本与理由]
**状态管理**：[Redux/Zustand/Context 实现方案]
**样式方案**：[Tailwind/CSS Modules/Styled Components]
**组件库**：[可复用组件结构]

## 性能优化
**Core Web Vitals**：[LCP<2.5s, FID<100ms, CLS<0.1]
**包体优化**：[代码分割与 tree shaking]
**图片优化**：[WebP/AVIF + 响应式尺寸]
**缓存策略**：[Service Worker + CDN]

## 无障碍实现
**WCAG 合规**：[AA 级 + 具体准则]
**屏幕阅读器**：[VoiceOver/NVDA/JAWS 兼容]
**键盘导航**：[全键盘可达]
**包容设计**：[prefers-reduced-motion + 对比度]
```

---

## 四、无障碍自动化（不是手动抽检）

- 无障碍**从组件开发第一天内建**（ARIA/语义 HTML/键盘导航），不是最后补
- 自动化 a11y 测试集成进 CI/CD（Lighthouse CI + axe）
- 真实辅助技术测试（VoiceOver/NVDA/JAWS）+ 神经多样性包容设计（动效偏好/对比度）

---

## 五、编辑器集成工程（特色能力，IDE/工具类产品用）

- 编辑器扩展导航命令（openAt/reveal/peek）+ WebSocket/RPC 桥接跨应用通信 + 协议 URI
- 导航动作 **sub-150ms 往返延迟** + 连接状态指示器

---

## 六、与 frontend-dev-guide 已有蒸馏的配合

| 文档 | 定位 |
|------|------|
| mvp-frontend-蒸馏（贾思敏） | CSS 工艺五条 + 代码级反 AI 门禁 |
| **frontend-developer-蒸馏（本文档）** | **性能量化基线 + 虚拟化 + 交付模板 + 无障碍 CI 化** |

> **使用原则**：实现大型列表/表格用本文档虚拟化模式；交付前按量化基线验收（CWV/Lighthouse/零 console error）；写交付文档用三节模板。

---

_蒸馏记录：v1.0（2026-09-06）· 专家「像素匠」→ frontend-dev-guide/expert-distill/_
