# 移动应用开发专家蒸馏 · Mobile Application Developer（掌中灵）

> **来源**：WorkBuddy 专家中心「掌中灵·移动应用开发」专家包蒸馏（2026-09-06）
> **源包**：`~/.workbuddy/plugins/marketplaces/experts/plugins/mobile-application-developer/agents/mobile-application-developer.md`（504 行）
> **蒸馏方式**：并入 frontend-dev-guide 的 expert-distill（前端延伸岗：App 开发）。
> **去重说明**：通用前端组件/性能方法论已由原生 + 其余蒸馏覆盖；本文档**只保留增量**——移动端三平台选型策略、移动性能量化基线、离线优先架构、平台集成清单、移动交付模板。三端框架代码示例（SwiftUI/Compose/RN）属落地示例，只提取规则。

---

## 一、三平台选型策略（先定架构再动手）

| 路线 | 框架 | 何时选 | 不选何时 |
|------|------|--------|----------|
| **iOS 原生** | Swift + SwiftUI | 仅 iOS 目标/深度系统集成（ARKit/Core Data） | 需双端 |
| **Android 原生** | Kotlin + Jetpack Compose | 仅 Android/复杂硬件交互 | 需双端 |
| **跨平台** | React Native / Flutter | 双端都要 + 团队熟悉 JS/Dart | 需要极深度平台原生能力 |

**默认建议**：MVP/工具类选跨平台（一套代码双端）；强平台体验/复杂原生能力选原生。**离线功能 + 平台适配导航是默认要求**（不是加分项）。

---

## 二、移动性能量化基线（验收标准）

| 指标 | 目标 |
|------|------|
| 冷启动时间 | < 3 秒（平均设备） |
| 崩溃率 | 无崩溃率 > 99.5%（全设备） |
| 内存占用 | 核心功能 < 100MB |
| 电池消耗 | 活跃使用 < 5%/小时 |
| 应用商店评分 | > 4.5 星（交付目标） |

**平台优化差异**：iOS 用 Metal 渲染 + Background App Refresh 优化；Android 用 ProGuard 混淆 + 电池优化豁免；跨平台控 bundle size + 代码共享策略。

---

## 三、离线优先架构（移动端必做设计）

1. **本地存储优先**：先写本地（Room/Core Data/AsyncStorage），网络是增强
2. **智能同步**：后台增量同步 + 冲突解决策略（时间戳/版本号）
3. **网络态处理**：弱网缓存 + 队列重试 + 断网可用核心功能
4. **列表分页**：FlatList/LazyColumn 无限滚动 + 分页阈值 0.5 + 渲染窗口控制（maxToRenderPerBatch=10、windowSize=21）
5. **平台阴影差异**：iOS shadow* 属性 / Android elevation（Platform.select 处理）

---

## 四、平台集成清单（按产品需要接入）

| 能力 | 说明 |
|------|------|
| 生物认证 | Face ID / Touch ID / 指纹（敏感操作必配） |
| 相机/媒体 | 拍照/图库/滤镜处理 |
| 定位/地图 | GPS / geofencing / 地图服务 |
| 推送通知 | APNs / FCM，带定向（不滥推） |
| 内购/订阅 | IAP / Play Billing（合规：苹果/谷歌抽成与审核） |
| 崩溃上报 | Crashlytics / Bugsnag（实时） |
| A/B 与灰度 | Feature Flag 框架（移动端灰度发布） |

---

## 五、移动交付模板（四节）

```
# [项目名] 移动应用
## 平台策略：目标平台（iOS 最低版本/Android 最低 API）/ 原生 or 跨平台理由
## 平台特定实现：iOS（SwiftUI/集成/ASO）· Android（Compose/集成/Play 优化）
## 性能优化：启动 <3s / 内存 <100MB / 电量 <5% 每小时 / 网络缓存与离线
## 平台集成：认证（生物）/ 相机 / 定位 / 推送 / 内购 / 崩溃上报
```

---

## 六、与 frontend-dev-guide 已有蒸馏的配合

| 文档 | 定位 |
|------|------|
| mvp-frontend-蒸馏（贾思敏） | Web CSS 工艺 + 反 AI 门禁 |
| frontend-developer-蒸馏（像素匠） | Web 性能基线 + 虚拟化 |
| **mobile-developer-蒸馏（本文档）** | **移动端（iOS/Android/RN/Flutter）：选型 + 性能基线 + 离线架构 + 平台集成** |

> **使用原则**：项目含 App 端时读本文档——先定平台路线（原生 vs 跨平台），性能按量化基线验收，默认做离线优先，集成能力按清单选配。

---

_蒸馏记录：v1.0（2026-09-06）· 专家「掌中灵」→ frontend-dev-guide/expert-distill/_
