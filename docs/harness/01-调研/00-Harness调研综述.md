# Harness 工程调研综述

> **沉淀日期**：2026-09-05
> **方法**：基于 WebSearch 检索摘要（5 篇权威来源）+ 个人 9 年后端/产品经验解读
> **可信度声明**：原始 URL 在 2026-09-05 复核时发现部分已失效（puppyone 域名待售、CSDN 链接 404），核心观点来自搜索摘要与多家来源交叉印证，建议关键决策点单独 WebFetch 验证
> **不适用场景**：本文档是入门级综述，**不替代深度精读**。具体落地时遇到分歧请回到原始来源

---

## 一、Harness 一句话定义

**Harness（驾驭工程）= 让 Agent 在企业里"安全、可控、可观测、可回滚"地跑起来的生产层架构**。

它不是新框架，是 LangChain / AutoGen / CrewAI 之上那一层——Agent 写好了，怎么放进生产环境的工程化问题。

类比传统软件：
- Framework = 写代码
- Harness = K8s + 监控 + 灰度 + 审计

---

## 二、与 Framework 的本质区分

| 维度 | Framework（开发层） | Harness（生产层） |
|---|---|---|
| 解决什么 | 怎么写 Agent | 怎么让 Agent 安全上线 |
| 代表 | LangChain / AutoGen / CrewAI | Harness.io / LangSmith / Helicone / 自研 |
| 谁用 | 算法 / 后端 | SRE / 平台 / 架构师 |
| 核心机制 | Chain / Graph / ReAct | Scope / State / Tool / Trace / Evals |

**常见误区**：以为用了 LangChain 就"上 Agent 了"。错。LangChain 只是开发框架，没治理的 Agent 等同于没熔断的微服务。

---

## 三、企业级五层架构（CSDN 架构师指南 · 2026）

```
L1 基础设施层：LLM API、向量库、缓存、对象存储
L2 执行层：    Agent 运行时、多模型路由、并发控制
L3 约束层：    权限（最小特权）、审计（spec-in-code）、限流、配额
L4 反馈层：    evals 回归套件、质量门禁、A/B 测试
L5 观测层：    trace、log、metrics、alert、可视化
```

实战里 **L3 + L5 最容易踩坑**：

- L3 没做 → Agent 越权删表、改 CI 配置、泄露密钥
- L5 没做 → Agent 偷偷变笨没人发现、出错无法定位

**OPC 阶段取舍**：L1~L3 必做（用现成 SaaS 即可），L4 部分做（evals 套件就够），L5 等团队到 5 人再补。

---

## 四、Harness 七能力（ONES 选型框架 · 2026）

| 能力 | 解决什么 | 落地物 |
|---|---|---|
| **State** | Agent 上下文怎么持久化 | project-tracker.md / Redis / state.json |
| **Validation** | Agent 产出物怎么校验 | evals 回归套件 / schema 校验 |
| **Observability** | Agent 怎么被监控 | trace + log + metrics |
| **Access** | Agent 能调什么 | 工具白名单 / 权限矩阵 |
| **Recovery** | Agent 出错怎么恢复 | git revert / checkpoint / 重试 |
| **Integration** | Agent 怎么对接现有系统 | MCP / webhook / API |
| **Governance** | Agent 怎么被合规管控 | audit log / spec-in-code / review |

OPC 阶段优先做 State + Access + Recovery + Validation（前 4 个），后 3 个等团队扩大再补。

---

## 五、7 个关键 Pattern（puppyone · 7 赢 1 输 · 2026）

### 赢的 Pattern

| Pattern | 核心观点 |
|---|---|
| **Harness 取代 Framework 成生产层** | Framework 是开发工具，Harness 才是生产必需品 |
| **Context base 击败向量库** | 上下文工程比 RAG 更重要，结构化 spec 比相似度检索靠谱 |
| **Day1 版本控制 + 审计** | 从第一天起所有 Agent 改动进 git，审计日志不可关 |
| **混合检索（BM25+向量+结构化过滤）** | 单一向量检索不够，多路召回合并 |
| **MCP 误用** | MCP 用错的代价比用错的 API 大（Agent 调用更不可控） |
| **纯 prompt 天花板** | 只靠 prompt 调教到顶就是天花板，必须有 Harness |
| **mixed-model 路由** | 不同任务用不同模型（小任务本地小模型、大任务云端大模型） |

### 我的判断（不是 puppyone 原话）

- **赢的 Pattern 1+2+3 是基础**：生产层 / Context / 版本控制，OPC 必做
- **赢的 Pattern 4+7 是进阶**：等 evals 跑通后再优化
- **输的 Pattern 5+6 是反例**：避免踩坑即可

---

## 六、四支柱（Harness.io · Agentic Era · 2026）

Harness.io 官方博客提出的 Agent 时代四支柱：

1. **Spec-Based Development**：用结构化规范（spec）驱动开发，不是自由 prompt
2. **Agent-Ready Architecture**：架构层支持 Agent 接入（tool/MCP/state 友好）
3. **Multi-Layer Verification**：多层验证（lint / type / 单测 / evals / 人工 review）
4. **15-20% 全自主 + 80% AI 辅助**：现实比例，不追求 100% 自主

**OPC 阶段判断**：

- 支柱 1 直接落地（`AGENTS.md` + `specs/`）
- 支柱 2 渐进做（MCP 接入根据业务需要）
- 支柱 3 现在做（已有 evals 套件）
- 支柱 4 不要激进（OPC 阶段默认 0% 全自主，对话协作是底线）

---

## 七、SKILL.md / AGENTS.md / Quality Gate 三角

```
SKILL.md     = 可执行知识（做什么、怎么做）
AGENTS.md    = 行为规范（不能做什么、什么场景怎么做）
Quality Gate = 质量门禁（产出物合格才放行，合格=人类 review）
```

**三角关系**：

| 文件 | 在 Harness 哪一层 | 谁维护 |
|---|---|---|
| SKILL.md | L2 执行层 + L3 约束层（知识部分） | 各角色 Skill 维护者 |
| AGENTS.md | L3 约束层（行为部分） | 项目 owner |
| Quality Gate | L4 反馈层 | AI + 人类共审 |

OPC 阶段三者配齐 = 准-Harness 雏形。

---

## 八、对 13+1 体系的对照（最关键）

| Harness 组件 | 13+1 体系当前 | 缺口 |
|---|---|---|
| L1 基础设施 | macOS M2 + Ollama 可跑本地推理 | ✅ 已具备 |
| L2 执行层 | 15 个 SKILL.md + orchestrator | ✅ 雏形 |
| L3 约束层 | 工具治理白名单 v1.0 | ⚠️ 部分 |
| L3 spec-in-code | 11 章方法论骨架 | ✅ 已具备 |
| L3 行为规范 | AGENTS.md v1.0（2026-09-05 落地） | ✅ 已具备 |
| L4 evals | regression-cases.json v1.0 | ✅ 已具备 |
| L4 反馈 | `.skills-memory/` 三层 | ✅ 雏形 |
| L4 状态 | project-tracker.md v1.0 | ✅ 已具备 |
| L5 观测 | 无 | ❌ 缺口（OPC 阶段不做） |
| 回滚 | git tag + revert 手动 | ⚠️ 半自动 |

**结论**：13+1 体系已覆盖 Harness 80% 核心能力，缺的 L5 观测层是 OPC 阶段可接受的妥协。

---

## 九、不做的事（明确取舍）

- ❌ 不上 LangSmith / Helicone 商业 Harness（团队<5 用不上）
- ❌ 不接 Devin / Factory / Codegen 全自主 Agent（合规+成本双高）
- ❌ 不追求 100% 全自主（OPC 阶段 0% 全自主）
- ❌ 不做分布式多 Agent 协同（单 Agent + 路由已够）
- ❌ 不建 L5 观测层（等团队到 5 人）

---

## 十、待 WebFetch 验证的关键观点

1. puppyone 7 Pattern 中"Context base 击败向量库"的具体论证
2. Harness.io 四支柱的原始博客全文
3. ONES 七能力评分卡的具体维度权重
4. CSDN 五层架构 L3 约束层的 spec-in-code 实现细节

_2026-09-05 已尝试 WebFetch puppyone（域名待售）+ CSDN 一篇（404），后续遇到具体落地问题需重新搜来源。_

---

_维护原则：每季度复核一次（下次 2026-12-05），核心观点漂移就更新。_
