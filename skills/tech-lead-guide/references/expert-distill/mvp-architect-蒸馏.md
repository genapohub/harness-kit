# MVP 团队·首席架构师蒸馏（高见远）

> **来源**：WorkBuddy「MVP 开发专家团」子角色「首席架构师·高见远」蒸馏（2026-09-06）
> **源包**：`git:mvp-dev-expert-team/agents/mvp-dev-expert-team-architect.md`（345 行）
> **蒸馏方式**：并入 tech-lead-guide 的 expert-distill。
> **去重说明**：ADR（MADR）、OpenAPI 契约、统一响应格式、Schema 原则等已由原生 `架构方法论.md` + software-architect 蒸馏覆盖；本文档**只保留增量**——MVP 技术选型权重（扩展性权重低！）、分场景栈表、搜索功能分级、Feature Flag 轻量灰度。

---

## 一、MVP 技术选型决策矩阵（反直觉权重）

> MVP 阶段选型权重与常规架构评审**不同**：扩展性权重低、团队熟悉度权重高。

| 维度 | 权重 | 评估标准 |
|------|------|----------|
| 学习成本 | 高 | MVP 阶段不选不熟悉的技术 |
| 生态成熟度 | 高 | 文档质量、社区活跃度、第三方库数量 |
| 部署成本 | 高 | 免费额度是否覆盖 MVP 阶段 |
| **扩展性** | **低** | **MVP 不需要未来 3 年的扩展性** |
| 团队熟悉度 | 高 | 用团队已经会的技术 |

**核心判断**：MVP 阶段"够用 + 团队会 + 部署便宜" > "架构完美 + 未来可扩展"。过早为 3 年后设计 = 浪费 MVP 的验证窗口。

## 二、MVP 分场景技术栈表

| 场景 | 前端 | 后端 | 数据库 | 部署 |
|------|------|------|--------|------|
| 国内 C 端 | Taro 3 | CloudBase 云函数 | 云开发数据库 | CloudBase |
| 国内 B 端 | React + Ant Design | NestJS + TypeScript | PostgreSQL | Docker |
| 海外 SaaS | Next.js | FastAPI (Python) | PostgreSQL + Redis | Vercel + Railway |
| 微信小程序 | Taro 3 / uni-app | CloudBase | 云开发数据库 | CloudBase |
| AI 产品 | Next.js | FastAPI | PostgreSQL + pgvector | Vercel |

### AI 产品专用栈 + pgvector MVP 方案

- **向量库首选 PostgreSQL + pgvector**（关系型+向量一体化，MVP 无需单独向量库）；大规模（百万级以上）才上 Milvus/Qdrant
- pgvector 落地：向量字段 `vector(1536)`（OpenAI embedding 维度）；查询 `ORDER BY embedding <=> '[...]' LIMIT 10`；索引：IVFFlat（<100 万）或 HNSW（>100 万）
- LLM 接入：OpenAI API / Claude API 按场景选

## 三、搜索功能分级设计（按数据量选方案）

| 场景 | 推荐方案 | 说明 |
|------|----------|------|
| 简单筛选（<1 万条） | PostgreSQL `ILIKE` + 索引 | MVP 首选，无需额外服务 |
| 中等搜索（1-10 万条） | PostgreSQL `tsvector` 全文检索 | 英文够用，中文分词支持差 |
| 复杂搜索（>10 万条） | Meilisearch / Elasticsearch | 独立搜索服务，支持中文分词 |
| AI 语义搜索 | pgvector 向量检索 | 见上 |

**落地 SQL（tsvector 全文检索）**：
```sql
ALTER TABLE tasks ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(description,''))) STORED;
CREATE INDEX idx_tasks_search ON tasks USING GIN (search_vector);
SELECT * FROM tasks WHERE search_vector @@ to_tsquery('english', 'design & system');
```

## 四、Feature Flag 灰度发布（MVP 轻量级，免第三方服务）

> MVP 上线后新功能必须走 Feature Flag 灰度，避免全量上线风险。

**轻量实现**：一张 `feature_flags` 表（key / enabled / rollouts{user_ids, percentage}）+ 后端中间件按 `hash(userId) % 100 < percentage` 放行 + 前端 `/api/features` 拉取状态。

**四阶段灰度策略**：

| 阶段 | 范围 | 持续时间 | 观察指标 |
|------|------|----------|----------|
| 内测 | 开发团队 user_ids | 1-2 天 | 功能正确性 |
| 小流量 | 5% 用户 | 3-5 天 | 错误率、性能 |
| 扩量 | 50% 用户 | 2-3 天 | 用户反馈、转化率 |
| 全量 | 100% | — | 移除 Flag |

## 五、机器可读产出物门禁（与原生 ADR/OpenAPI 呼应）

- **无 `openapi.yaml` 不放行开发阶段**：前后端以此为唯一契约（前端据此生成 TS 类型 + Mock，后端据此实现）；变更走 spec 更新 + 同步
- ADR 用 MADR 格式（Status/Background/Decision/Consequences/Related），存 `docs/decisions/ADR-XXX.md`

## 六、与原生方法论的配合

| 场景 | 用哪个 |
|------|--------|
| 场景识别 / 产出清单 / ADR / 交付衔接 | `架构方法论.md`（原生，主） |
| 领域建模 / 模式选型 | software-architect-蒸馏（架构通） |
| 后端数据/API/可靠性细节 | backend-architect-蒸馏（磐石石） |
| **MVP 阶段选型权重 / 分场景栈 / 搜索分级 / Feature Flag 灰度** | **本文档（增量，唯一来源）** |

> **使用原则**：技术选型章节涉及 MVP/快速验证项目时，用本文档一的权重表（扩展性低权重）覆盖常规评审逻辑；架构中含搜索或灰度需求时查本文档三四节。

---

_蒸馏记录：v1.0（2026-09-06）· MVP 专家团「首席架构师·高见远」→ tech-lead-guide/expert-distill/_
