# 后端架构师专家蒸馏 · Backend Architect（磐石石）

> **来源**：WorkBuddy 专家中心「磐石石」专家包蒸馏（2026-09-06）
> **源包**：`~/.workbuddy/plugins/marketplaces/experts/plugins/backend-architect/agents/backend-architect.md`（242 行）
> **蒸馏方式**：方法论精华提炼，并入 tech-lead-guide 的 expert-distill。
> **去重说明**：微服务/事件驱动/Serverless 选型已由 software-architect 蒸馏 + 原生架构方法论覆盖，本文档聚焦**后端/数据/API/安全的落地规范与量化框架**。
> **配合关系**：software-architect 蒸馏 = 宏观架构与领域设计；本文档 = 后端系统的工程化细节。

---

## 一、后端架构成功指标（量化基线）

> 设计后端系统时先立目标数字，再谈方案——没有数字的架构是空谈。

| 指标 | 目标 | 验证方式 |
|------|------|---------|
| API 响应时间 | P95 < 200ms | 压测报告 |
| 系统可用性 | > 99.9%（月不可用 < 43 分钟） | 监控 SLA |
| 数据库查询 | 平均 < 100ms（含索引后） | 慢查询日志 |
| 安全审计 | 0 关键漏洞 | 安全扫描 |
| 峰值承载 | 10x 正常流量不掉 | 容量压测 |
| 扩展性 | 加机器线性提升 | 水平扩缩容演练 |

---

## 二、数据 / Schema 工程规范

### 2.1 Schema 设计铁律

1. **主键用 UUID 而非自增**——避免枚举泄露 + 支持分布式生成
2. **软删除标配**：`deleted_at TIMESTAMP NULL`，唯一索引加 `WHERE deleted_at IS NULL`
3. **时间戳统一**：`TIMESTAMP WITH TIME ZONE`（UTC 存储），`created_at` / `updated_at` 必带
4. **约束进 DB 不进代码**：`CHECK (price >= 0)`、`UNIQUE`、`FOREIGN KEY` 都写在 schema——代码校验能绕过，DB 约束不能
5. **部分索引**：高频查询条件（如 `is_active = true`）用 `WHERE` 部分索引减小体积
6. **全文检索**：名称/描述用 GIN 索引（`to_tsvector`）而非 `LIKE '%x%'`
7. **向后兼容**：schema 变更必须考虑存量数据；加列可以，改语义要迁移脚本 + 双写过渡

### 2.2 十亿级/10 万+ 实体设计要点

- 规范化到第三范式，但**为高频查询保留受控冗余**（如订单快照商品名）
- 读写分离：读多写少的表加只读副本
- 冷热分离：热数据在 PostgreSQL/Redis，冷数据归档对象存储
- 分片只在大表真的扛不住时做，先试分区表（partition by range）

---

## 三、架构交付物四维模板（快速起稿）

> 每份系统架构设计文档，先填这四维再展开细节：

```
**Architecture Pattern**:  Microservices / Monolith / Serverless / Hybrid
**Communication Pattern**: REST / GraphQL / gRPC / Event-driven
**Data Pattern**:          CQRS / Event Sourcing / Traditional CRUD
**Deployment Pattern**:    Container / Serverless / Traditional

服务拆解（每个核心服务给 3 行）：
**{Service} Service**: 职责一句话
- Database: {用什么 + 特殊配置，如 read replicas / ACID}
- Cache:    {缓存什么，为什么}
- APIs:     {风格 + 特殊，如 webhook 回调}
- Events:   {对外发什么事件}
```

---

## 四、API 设计安全基线（纵深防御）

> 以下是不依赖具体框架的通用基线，任何后端 API 都应具备：

| 层 | 措施 | 目的 |
|----|------|------|
| **传输** | TLS + HSTS | 防窃听 |
| **入口** | Rate Limiting（IP + 用户双维度） | 防滥用/爆破 |
| **头部** | 安全响应头（helmet 类：CSP/X-Frame-Options 等） | 防注入/点击劫持 |
| **认证** | OAuth 2.0 / JWT 短时 + refresh | 身份可信 |
| **授权** | RBAC 最小权限，接口级校验 | 越权防护 |
| **数据** | 静态加密 + 敏感字段加密存储（密码 bcrypt） | 防拖库 |
| **错误** | 统一错误格式：`{ error, code }`，不吐堆栈 | 防信息泄露 |
| **审计** | 敏感操作（登录/删除/转账）留 audit log | 可追溯 |

**统一错误格式约定**：`{ "error": "人类可读", "code": "MACHINE_CODE", "details": {...} }`，HTTP 状态码语义化（400 参数错 / 401 未认证 / 403 无权限 / 404 不存在 / 409 冲突 / 429 限流 / 5xx 服务错）。

---

## 五、可靠性清单（上线前逐项过）

- [ ] 关键路径有熔断器（下游 5xx 率 > 阈值即熔断）
- [ ] 失败有重试策略（指数退避 + 抖动，幂等性保证）
- [ ] 有优雅降级（缓存兜底 / 功能开关可关非核心功能）
- [ ] 备份策略（RPO/RTO 定义清楚）+ 恢复演练定期做
- [ ] 监控告警（错误率/延迟/资源水位/连接池），告警有责任人
- [ ] 自动扩缩容规则（指标 + 阈值 + 冷却时间）
- [ ] 队列消费有死信处理 + 重放机制

---

## 六、缓存策略纪律

1. **缓存是优化不是默认**——先量后缓：没数据证明热点就不加缓存
2. **缓存不引入一致性问题**：设 TTL 兜底、写后失效（cache-aside）优先于先写缓存
3. **缓存层级**：本地（进程内）→ 分布式（Redis）→ CDN，每层明确缓存什么
4. **缓存击穿/穿透/雪崩** 三个反模式必须有应对（空值缓存/布隆过滤器/过期时间打散）

---

## 七、与本地方法论及软件架构蒸馏的配合

| 场景 | 用哪个 |
|------|--------|
| 场景识别 / 产出清单 / ADR / 交付衔接 | `架构方法论.md`（原生，主） |
| 领域建模 / 模式选型（单体 vs 微服务等） | software-architect-蒸馏（架构通） |
| **后端数据 Schema 设计 / API 安全基线 / 可靠性清单 / 缓存纪律** | **本文档（唯一来源）** |
| 后端技术选型（DB/缓存/队列横向对比） | 原生技术选型评估维度 |

> **使用原则**：tech-lead-guide 被用于后端系统设计/评审时，先读原生 `架构方法论.md` 定位场景，再读 software-architect 蒸馏拿领域/模式框架，落地数据/API/可靠性细节时查本文档。

---

_蒸馏记录：v1.0（2026-09-06）· 专家「磐石石」→ tech-lead-guide/expert-distill/_
