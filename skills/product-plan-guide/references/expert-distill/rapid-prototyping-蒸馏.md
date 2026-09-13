# 快速原型验证方法论 · 专家蒸馏（闪造造·Rapid Prototyper）

> **并入宿主**：`product-plan-guide`（产品经理技能）——作为方案文档产出后的**快速验证衔接层**：PRD 写完不等于验证完，用可运行原型把假设落地验证。
> **蒸馏来源**：WorkBuddy 专家中心「闪造造·快速原型工程师」专家包（2026-09-06，agents 468 行）。
> **去重说明**：本文档只保留"产品需求 → 可运行验证"的方法论增量；正式工程开发（前后端分层/架构）由 frontend/backend-dev-guide 承接，不重复。

---

## 一、场景识别

| 场景 | 名称 | 判断条件（满足任一） | 交付物 | 预估周期 |
|------|------|---------------------|--------|---------|
| 场景一 | 一句话想法验证 | 只有一个模糊想法、无任何文档 | 可运行 demo + 假设清单 | 1-2 天 |
| 场景二 | PRD 转可运行 MVP | 已有 PRD/需求文档、要看到能跑的产品 | 核心流程 MVP | 3 天 |
| 场景三 | 单功能原型 | 现有产品加功能、先验证交互 | 单页可点击原型 | 1 天 |
| 场景四 | 设计稿转交互原型 | 已有高保真稿、要可点击测试 | 高保真交互原型 | 2-3 天 |
| 场景五 | 原型转生产评估 | 原型已跑通、评估演进 vs 重写 | 评估报告 | 1 天 |

### 识别流程

```
有无文档？
├── 无 → 场景一（一句话想法）
├── 有 PRD/需求 → 场景二（转 MVP）
└── 有设计稿 → 场景四（转交互原型）
     ↓
是现有产品加功能？→ 场景三
是已跑通要评估生产化？→ 场景五
```

---

## 二、技术栈速查（2026 快速原型默认栈）

### 默认栈（无特殊约束就用这套）

```
前端：    Next.js 14 (App Router) + TypeScript + Tailwind CSS
UI 组件： shadcn/ui（预构建、可复制、无锁）
表单：    react-hook-form + zod（schema 校验一体）
状态：    zustand（轻量，够用）
动效：    framer-motion（加分项，非必需）
数据库：  PostgreSQL + Prisma ORM（schema 即文档）
BaaS：    Supabase（认证/存储/实时 一键）
认证：    Clerk（社交登录 3 行接入）
部署：    Vercel（零配置 + 预览 URL）
埋点：    自建 /api/analytics + 事件表（避免引 SDK 拖慢）
```

### 按场景调栈

| 场景 | 调整 |
|------|------|
| 纯前端 demo（无用户系统） | 砍 Clerk/DB，Vercel 静态部署即可 |
| 表单密集型 | 优先 react-hook-form + zod（模板化快） |
| 实时类（聊天/协作） | Supabase Realtime 或 WebSocket |
| 数据看板类 | 直连 Supabase + 图表库（recharts） |
| 国内部署 | Vercel 换腾讯云/边缘部署，认证换微信登录 |
| 无代码更快的场景 | 评估 Airtable/Bubble/墨刀 等低代码，别硬编码 |

### 选型三原则

1. **能白嫖的用现成的**：认证/部署/存储全部 BaaS 化，不自己搭
2. **一个库一个职责**：不引全家桶；装了就用的才装
3. **默认栈不纠结**：没有特殊约束就 Next.js 全家桶，纠结 30 分钟以上=浪费

---

## 三、工程搭建清单（Day 1 地基）

### 3.1 项目结构（参照 backend-dev-guide 分层，精简版）

```
project/
├── app/                  # Next.js App Router 页面
│   ├── (auth)/           # 登录注册（Clerk 布局）
│   ├── (main)/           # 主流程页面
│   └── api/              # 路由处理器
├── components/
│   └── ui/               # shadcn/ui 组件
├── lib/
│   ├── analytics.ts      # 埋点 helper
│   ├── ab-test.ts        # A/B 分配 hook
│   └── db.ts             # Prisma client
├── prisma/
│   └── schema.prisma     # 数据模型
└── .env.example          # 环境变量样例（假值）
```

### 3.2 Prisma schema 模板（含反馈模型）

```prisma
generator client { provider = "prisma-client-js" }
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String     @id @default(cuid())
  email     String     @unique
  name      String?
  createdAt DateTime   @default(now())
  feedbacks Feedback[]
  @@map("users")
}

model Feedback {
  id        String   @id @default(cuid())
  content   String
  rating    Int
  userId    String
  user      User     @relation(fields: [userId], references: [id])
  createdAt DateTime @default(now())
  @@map("feedbacks")
}
```

### 3.3 埋点 helper（Day 1 必装）

```typescript
export function trackEvent(eventName: string, properties?: Record<string, any>) {
  if (typeof window !== 'undefined') {
    window.gtag?.('event', eventName, properties);          // GA4（如已接）
    fetch('/api/analytics', {                               // 自建兜底
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event: eventName, properties, timestamp: Date.now(), url: window.location.href }),
    }).catch(() => {});                                     // 静默失败，不阻塞用户
  }
}
```

### 3.4 A/B 测试 hook（关键转化点用）

```typescript
export function useABTest(testName: string, variants: string[]) {
  // 1. 取/建稳定 user_id（localStorage，crypto.randomUUID）
  // 2. 简单哈希取模分桶：variantIndex = |hash(userId)| % variants.length
  // 3. 上报 ab_test_assignment（test_name + variant）
  return assignedVariant;
}
```

> 原则：原型期 A/B 用"简单哈希分桶"，不引重 SDK。统计显著性在样本不足时如实标注，不硬凹结论。

---

## 四、4 步执行节奏（3 天交付）

### Day 1 上午：需求 + 假设定义

三问定盘（不问够就开始做 = 返工源头）：
1. 核心假设是什么？→ 写进假设清单第一行
2. 给谁测？→ 明确测试用户池（内部/种子用户/外部）
3. 成功长什么样？→ 量化成功指标

**假设清单模板**：

```
核心假设：{一句话}
成功指标：{可量化，如 "80% 测试者完成核心流程"}
最小功能集：{3-5 个，只留验证假设的}
不做清单：{明确砍掉，防膨胀}
```

### Day 1 下午：地基搭建

按第三节清单逐项过（脚手架/认证/DB/埋点/部署），拿预览 URL。

### Day 2-3：核心功能

- 核心用户流程优先（登录 → 主操作 → 结果页）
- shadcn/ui 快拼界面，视觉默认样式
- 数据模型 + API 端点 + 基本校验
- 关键转化点埋点 + A/B

### Day 3-4：用户测试 + 迭代

- 给测试者分享 URL + 引导语（"重点试 X，看 Y 是否顺畅"）
- 收集数据 + 应用内反馈
- 输出验证报告

---

## 五、原型转生产判断（场景五）

| 判断维度 | 演进成生产 | 重写 |
|---------|-----------|------|
| 代码质量 | 分层清晰、可测试 | 面条代码、硬编码遍地 |
| 假设验证 | 已验证核心假设、指标达标 | 还在大幅 Pivot，方向未定 |
| 数据模型 | 与真实业务模型接近 | 原型数据模型是"演示专用" |
| 用户量级 | 冷启动小规模可扛 | 预期量级远超原型架构 |
| 时间压力 | 需要快速上线抢窗口 | 有重构窗口 |

**默认建议**：原型走完验证后**大多数值得重写**（除非代码质量好且假设已稳）——原型的技术债是"故意欠的"，别让它进生产。

---

## 六、交付质量检查清单

- [ ] 有可分享 URL（不是代码包）
- [ ] 核心流程完整走通（无死链/空页面）
- [ ] 埋点事件表已定义且能看数据
- [ ] 反馈收集通道已开（应用内/表单/联系方式）
- [ ] 假设清单有明确验证结论（✅/⚠️/❌）
- [ ] 不做清单被执行（没悄悄加功能）
- [ ] 未使用真实生产数据/密钥
- [ ] 明确给出转生产判断（演进 or 重写 + 理由）

### 去 AI 味自检（交付前强制）

- [ ] 是否明确说了"这个原型不做什么"？
- [ ] 假设是否一句话说清（不是"提升用户体验"这种空话）？
- [ ] 是否承认了视觉是临时的（没假装是最终稿）？
- [ ] 是否如实标注了数据不足/样本不够（没硬编结论）？

---

## 七、超越 AI 味：快速原型工程师的真实判断

> AI 能"假装"做了个原型（给文档/给截图/给代码但不给能跑的 URL），真正的快速原型工程师交付的是**别人能点的东西**。

1. **原型不是演示 PPT**：没有 URL 的原型交付 = 没交付。所有产出必须"能跑"
2. **砍功能是核心能力**：用户说"顺便加个 XX"，反问"它验证哪个假设？"答不出就砍
3. **3 天是纪律不是目标**：第 4 天还没交付，砍功能而不是延时间——范围膨胀是原型失败第一原因
4. **粗糙但真实 > 精致但假**：能点的丑原型比不能点的漂亮稿有价值 100 倍
5. **诚实标注数据限制**：原型期样本量小，结论要标注"基于 N 个测试者"，不硬装统计显著

---

_技术负责人的反面：把原型做成"准生产"、把 3 天拖成 3 周、把验证做成自嗨。_

---

_蒸馏记录：v1.0（2026-09-06）· 专家「闪造造·Rapid Prototyper」→ product-plan-guide/expert-distill/（并入产品经理技能，验证闭环）_
