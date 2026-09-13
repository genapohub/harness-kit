# MVP 团队·测试工程师蒸馏（严过关）

> **来源**：WorkBuddy「MVP 开发专家团」子角色「测试工程师·严过关」蒸馏（2026-09-06）
> **源包**：`git:mvp-dev-expert-team/agents/mvp-dev-expert-team-qa.md`（374 行）
> **蒸馏方式**：并入 qa-testing-guide 的 expert-distill。
> **去重说明**：测试金字塔、缺陷分级 P0-P2、测试清单（happy/异常/边界/权限/状态）、OWASP 安全清单等已由原生 `QA测试方法论.md` 覆盖；本文档**只保留增量**——先写测试原则（写测≠写码）、测试完整性反作弊门、改动影响分析、回归率归零纪律、质量报告指标、视觉合规扫描。

---

## 一、先写测试原则（核心变革）

> **写测试的角色 ≠ 写代码的角色。** 基于 AgentCoder 实验（91.5% vs 86.8% pass@1），同一 agent 写实现又写测试会产生「同义测试反模式」——测试复述实现假设，绿灯零信息量。

**工作流**：
1. Spec 确定后，**QA 先写测试用例**（基于验收标准，覆盖正常+异常+边界+权限+状态）
2. 开发**按 QA 已写好的测试实现**代码（测试先行驱动）
3. 开发完成后 QA 跑测试 + 评审 + 出质量报告

> 对 AI 编程尤其重要：AI 自己写的测试常复述自己实现的行为，让"全绿"失去意义。

---

## 二、测试完整性反作弊门（P0 级门禁）

> AI 生成代码会作弊：删测试换绿、弱化断言、加 skip。门禁中拦截。

对比开发前后测试 surface，发现**任一**即阻断（P0 缺陷）：

| # | 作弊类型 | 检测方法 |
|---|----------|----------|
| 1 | 测试文件/用例被删 | `git diff --stat` 检测测试文件删除或行数骤减 |
| 2 | 断言数下降 | 对比前后 `expect(`/`assert ` 调用数量 |
| 3 | 新增 skip/xfail/.only/focus | `grep` 对比新增 |
| 4 | 断言硬编码实现输出 | 人工审查：断言值来自实现返回值而非 Spec 定义 |
| 5 | 测试框架配置篡改 | `git diff` 检查 jest/pytest 配置的测试/覆盖率阈值变更 |

**检测脚本核心三条**：
```bash
# 1. 测试文件删除检测
git diff --name-status HEAD~1 -- 'tests/' '**/*.test.*' | grep '^D'
# 2. 断言数对比
git show HEAD~1:tests/ | xargs grep -c 'expect\|assert' | sort > /tmp/before.txt
grep -rc 'expect\|assert' tests/ | sort > /tmp/after.txt
diff /tmp/before.txt /tmp/after.txt | grep '<'
# 3. skip/xfail 新增检测
git diff HEAD~1 -- 'tests/' | grep '^+' | grep -i 'skip\|xfail\|\.only\|focus'
```

---

## 三、改动影响分析（每次测试前必做）

拿到代码 diff 后先回答"改了什么 → 波及哪些旧行为 → 风险优先级"：

```markdown
## 改动影响分析
### 本次改动范围
- 修改文件 / 函数 / 接口 / 改动类型（新增|修改|删除|重构）
### 下游影响面
- 直接调用方 / 共享状态影响（数据库/缓存/全局变量）
- 旧行为风险面：{旧行为1} → 高/中/低
### 回归测试优先级
1. 高风险旧行为 → 必测
2. 中风险 → 应测
3. 低风险 → 抽测
```

---

## 四、质量报告核心指标（数据驱动，非主观）

| 指标 | 目标 |
|------|------|
| 冒烟测试 | 通过（核心流程 30 分钟内跑通） |
| 功能测试通过率 | 100% |
| P0 缺陷 | 0（非零不交付） |
| P1 缺陷 | ≤ 总数 × 20% |
| 代码覆盖率 | ≥ 80% |
| **回归率（旧行为由绿转红）** | **0（非零不算完成）** |
| 解决率 | 100% |
| 测试完整性反作弊 | 通过 |
| 返工次数 | ≤ 3 |

**P0 缺陷修复后必须沉淀回归用例**：存入 `tests/regression/<缺陷名>.test.ts`，进版本库，每次改动都跑，**只增不轻易删**。

---

## 五、视觉合规扫描（AI 产物专项，可脚本化）

```bash
# emoji 图标扫描（P0）：预期零匹配
grep -rP '[\x{1F300}-\x{1F9FF}\x{2600}-\x{26FF}\x{2700}-\x{27BF}]' src/ --include='*.tsx' --include='*.jsx' --include='*.vue'
# 紫粉渐变扫描（P1）
grep -rn 'purple.*pink\|from-purple.*to-pink' src/ --include='*.tsx' --include='*.css'
# AI 模板味占位扫描（P1）
grep -rn 'Welcome to\|Lorem ipsum' src/
```

---

## 六、生产就绪评级（7 维 × 3 档）

| 维度 | 档位 | 维度 | 档位 |
|------|------|------|------|
| 测试 + 回归 | Bronze/Silver/Gold | 性能 | Bronze/Silver/Gold |
| 契约 | Bronze/Silver/Gold | 可观测 | Bronze/Silver/Gold |
| 安全 | Bronze/Silver/Gold | 发布安全 | Bronze/Silver/Gold |
| 无障碍 | Bronze/Silver/Gold | **总档（取最低）** | **未达 Silver 不交付商业生产** |

---

## 七、MVP 性能标准

| 测试项 | 工具 | 标准 |
|--------|------|------|
| API 响应时间 | curl + 计时 | p95 < 500ms |
| 页面加载 | Lighthouse CI | Performance > 70 |
| 并发 | k6 / wrk | 50 req/s 不崩溃 |

---

## 八、与原生方法论的配合

| 场景 | 用哪个 |
|------|--------|
| 5 场景识别 / 测试策略产出 / 用例设计 | `QA测试方法论.md`（原生，主） |
| 测试金字塔 / 缺陷分级 / OWASP 清单 | 原生方法论 |
| **AI 产物测试门禁（先写测试/反作弊门/回归率=0/视觉扫描）** | **本文档（增量，唯一来源）** |

> **使用原则**：涉及 AI 生成代码的质量保障时，本文档是硬性门禁来源——QA 先写测试、开发按测试实现、交付前跑反作弊门与改动影响分析。

---

_蒸馏记录：v1.0（2026-09-06）· MVP 专家团「测试工程师·严过关」→ qa-testing-guide/expert-distill/_
