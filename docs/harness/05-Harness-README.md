# 05-Harness · Harness 工程实践

> 企业级 AI 编程治理架构（Agent 生产层）的本地沉淀目录。
> 配套 13+1 角色技能体系，把"技能库"升级为"准-Harness 工程"。

---

## 一、目录定位

解决的不是"模型能力"问题，是"Agent 怎么在企业里安全、可控、可观测、可回滚地跑起来"的工程问题。

```
技能层（已有）  →  执行层（已有）  →  约束层（本目录）  →  反馈层（本目录）  →  观测层（待建）
13+1 SKILL.md     orchestrator       AGENTS.md            evals/              trace/log/metrics
                                   工具治理白名单          project-tracker
```

---

## 二、子目录规划

| 子目录 | 用途 | 状态 | 内容 |
|---|---|---|---|
| `01-调研/` | Harness 概念与选型 | ✅ 已建 | 3 份笔记：综述 / 5 篇来源索引 / 13+1 体系行动启示 |
| `02-规范/` | AGENTS.md / CLAUDE.md / .cursorrules 等模板 | ✅ 已建 | AGENTS.md v1.0（10 部分 + 3 附录 + Harness 版本管理段）+ SECURITY.md v1.0（10 部分，密钥/脱敏/合规三件套） |
| `03-状态/` | project-tracker / state 持久化 | ✅ 已建 | project-tracker.md v1.0（9 部分） |
| `04-Evals/` | 回归测试套件 | ✅ 已建 | regression-cases.json v1.0（14 case / 6 类）+ runner.py v0.3（4 case 自动化 + 豁免规则 + 增量模式） |
| `05-Skills/` | 本地角色技能接入层 | ✅ 已建 | `--with-local-skills` 从 `日常办公/00-Skills汇总` 安装真实技能到项目 `skills/` |
| `05-实战/` | 真实项目落地记录 | ✅ 已建 | 宠宝树试点 v1.0（装机 + 首个 evals 闭环，增量 3/3 全绿，2026-09-05） |
| `06-Adapters/` | 多 AI 工具适配模板 | ✅ 已建 | Claude / Cursor / GitHub Copilot / Kiro 适配文件，装机时 `--with-adapters` 可选生成 |
| `06-工具链/` | 工具治理白名单 + 脚本 | ✅ 已建 | 工具治理白名单 v1.1（P0 常驻 6 角色 / P1 阶段激活 3 / P2 挂起 6 + 红线 8 条）+ MCP-工具分级 v1.0（132 工具 L1~L5 分级 + 决策矩阵 + 审计 SOP）+ skill-library-selfcheck.py（技能库 7 维自检）+ harness-kit-sync-check.py（05↔06-kit 模板对齐核查：文件级 + 内容级双层，覆盖 05-Skills / 06-Adapters） |
| `07-Kit/` | 一条命令装机脚本 | ✅ 已建 | install.sh v1.5：三件套落位项目根 + 可选本地 Skills + 可选多工具适配 + git init + harness tag |
| `README.md` | 本文件 | ✅ | 目录索引 |

---

## 三、与 13+1 体系的关系

13+1 角色技能体系已经覆盖 Harness 的 L2 执行层（spec-in-code）+ L2 调度编排（team-orchestrator）。

本目录承载 L3 约束层 + L4 反馈层，补齐"治理三件套"：

| Harness 治理件 | 本目录承载物 | 落地优先级 |
|---|---|---|
| 工具治理（白名单/审批/限流） | `06-工具链/` | P0 |
| 持久化状态（State） | `03-状态/project-tracker.md` | P0 |
| 评估反馈（evals） | `04-Evals/` | P1 |
| 回滚机制（rollback） | `05-实战/` 配 git tag | P1 |
| 观测层（trace/log） | 暂不建（等真实项目跑通后补） | P2 |

---

## 四、当前进度（2026-09-06）

- ✅ 01-调研/：4 份笔记（综述 / 5 篇来源索引 / 13+1 体系行动启示 / 五层架构文件分层对照）
- ✅ 02-规范/：AGENTS.md v1.4（10 部分 + 3 附录 + 附录 C 版本管理；v1.4 新增「角色状态」一人双角色开工声明：PM_脑/Dev_脑 显式切换 + tracker 留痕）+ SECURITY.md v1.0（密钥/脱敏/合规三件套）
- ✅ 03-状态/：project-tracker.md v1.0（9 部分）
- ✅ 04-Evals/：regression-cases.json v1.0（14 case / 6 类；usage 含豁免机制：存量=基线 + 内置豁免清单 + 新增豁免须人工确认）+ runner.py v0.3（Harness 三件套检查 + 增量模式 + 豁免规则）
- ✅ 05-Skills/：本地角色技能接入说明，支持装机时复制 `00-Skills汇总` 真实技能
- ✅ 05-实战/：宠宝树试点 v1.0（2026-09-05 装机 + 首个 evals 闭环 253→0）+ pet_xiaoman 开发复盘 v1.0（v1.3 工作纪律迭代依据）
- ✅ 06-Adapters/：Claude / Cursor / GitHub Copilot / Kiro 适配模板
- ✅ 06-工具链/：工具治理白名单 v1.1（P0 常驻 6 / P1 阶段 3 / P2 挂起 6 + 红线 8 条）+ MCP-工具分级 v1.0（132 工具 L1~L5）+ skill-library-selfcheck.py（技能库 7 维自检）+ harness-kit-sync-check.py（05↔kit 双源模板对齐核查）
- ✅ 07-Kit/：install.sh v1.5（一条命令装机 + 本地 Skills 接入 + 多工具适配 + Day1 git init + harness tag）
- ✅ 与 06-harness-kit 双源同步：模板 v1.5 两侧一致（sync-check ALL CLEAR，差异仅母体定制/分发通用预期分化）
- ⬜ L5 观测层（trace/log/metrics）：等真实项目跑通后补（P2 暂缓）
- ⬜ kit 装机第二实测：待新项目 Day1 装机验证 v1.4 角色状态（暂缓）

---

## 五、明确"做"与"不做"

| 决策 | 做不做 |
|---|---|
| 从 `02-规范/AGENTS.md` 起步 | ✅ 做 |
| 选 product-plan-guide + b2b-need-mining-guide 两个角色做 Agent 试点 | ✅ 做（OPC 变现路径） |
| 把 orchestrator 升级为 Harness 治理层 | ✅ 做（单点突破 ROI 最高） |
| 13 个角色全 Agent 化 | ❌ 不做（工程量大、收益边际递减） |
| 13+1 角色全量纳入每个项目治理 | ❌ 不做（2026-09-05 起 v1.1 按 P0/P1/P2 分级激活，P0 常驻仅 6 角色；项目宪法只约束激活角色） |
| 接 Devin/Factory/Codegen 全自主 Agent | ❌ 不做（OPC 阶段） |
| 建 LangSmith/Helicone 商业 Harness | ⚠️ 暂缓（团队<5 用不上） |
| 全员强制用 AI 编程 | ❌ 不做（先自愿试点） |

---

## 六、下一步具体动作（推荐顺序）

1. **建 `02-规范/AGENTS.md` 模板**（30 分钟）：项目根目录 AI 行为规范
2. **建 `03-状态/project-tracker.md`**（30 分钟）：Harness state 层从 0 到 1
3. **写 `06-工具链/工具治理白名单.md`**（1 小时）：每个角色 SKILL.md 补"禁止调用工具清单"
4. **建 `04-Evals/regression-cases.json` 骨架**（1 小时）：固化 AI 生成代码的回归测试基线

---

_本目录遵循"先骨架再追加细节"模式（用户已确认的迭代规范），每个文件先建空壳再补内容。_
