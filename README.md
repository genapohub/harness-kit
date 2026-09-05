# harness-kit · AI 编程治理脚手架

> 一条命令，把「AI 行为宪法 + 项目状态单一事实源 + 安全红线 + 产出物回归测试」装进任何项目根目录，
> 让 Cursor / Claude Code / Codex / ZCode 等所有支持 AGENTS.md 规范的 AI 编程工具，在你的规则里干活。
>
> **One command to harness your AI coding agents: AGENTS.md constitution + project state + security rules + evals.**

---

## 一、解决什么问题

裸奔使用 AI 编程工具的三个典型事故：

| 痛点 | 后果 | harness-kit 的对策 |
|---|---|---|
| AI 不了解项目就盲改代码 | 改坏架构、破坏约定 | `AGENTS.md` 项目宪法：进入项目必须先读身份 YAML，AI 能做/不能做/怎么干活写得明明白白 |
| AI 调用不该调的工具（rm -rf、碰 .env、push main） | 不可逆事故 | 红线清单 + 工具白名单：越权即拒绝，不许"勉强执行" |
| AI 产出质量悄悄劣化没人发现 | 技术债滚雪球 | evals 回归套件：13 个 case 定期跑，劣化即拦截 |

一句话：**Framework 解决"AI 怎么写代码"，harness-kit 解决"AI 怎么安全、可控、可回滚地在你的项目里干活"。**

## 二、快速开始（30 秒装机）

```bash
git clone https://github.com/genapohub/harness-kit.git
bash harness-kit/07-Kit/install.sh /path/to/你的项目
```

就这两步。脚本会自动完成：

1. 三件套落位到项目根目录：`AGENTS.md` + `project-tracker.md` + `SECURITY.md`
2. 占位符自动填充（项目名、日期、责任人取自你的 `git config user.name`、P0 激活角色）
3. 模板里指向本仓库的引用改写为你机器上的绝对路径（不断链）
4. 检测项目内嵌套的独立 git 仓库并从根仓库隔离（.gitignore，互不污染）
5. `git init`（main 分支）+ 初始 commit + `harness-vX.Y` tag——Day1 版本控制

装机完成后按脚本输出的手工待办补 3 处（约 5 分钟）：项目身份 YAML、按需勾选 P1 角色、tracker 阶段总览一句话。

> **防覆盖**：目标项目已有 `AGENTS.md` 时脚本自动中止。**支持范围**：macOS / Linux（bash + git + python3），Windows 建议 WSL。

## 三、装机后你会得到什么

```
你的项目/
├── AGENTS.md                  ← 宪法：AI 能做什么/红线/10 步工作流（所有 AGENTS.md 系工具自动读取）
├── project-tracker.md         ← 状态单一事实源：WIP/决策日志/Agent 间交接上下文
├── SECURITY.md                ← 安全子法：密钥分级/数据脱敏/模型路由合规
├── .gitignore                 ← .DS_Store + AI 工具记忆目录 + 嵌套仓库隔离
└── .git（tag: harness-v1.1）  ← 治理资产从第一天进版本控制
```

| 文件 | 谁读 | 什么时候 |
|---|---|---|
| `AGENTS.md` | Cursor / Claude Code / Codex / ZCode 自动读根目录，子目录工作向上查找 | 每次对话 |
| `project-tracker.md` | AI 按宪法要求开工先读、收工更新 | 每个任务 |
| `SECURITY.md` | 涉及密钥/客户数据/外发时按它执行 | 触发场景 |

## 四、日常怎么用：任务闭环 5 步

1. **开工喂上下文**：开场第一句
   > 先读 AGENTS.md 和 project-tracker.md 的「AI 协作上下文」段，复述你理解的任务和边界，确认后再动手。
2. **盯住工作流两个关键步**：AI 复述需求（不懂就问，不许猜）、等人类 review（不批不合并），跳步 = 越权
3. **白名单兜底**：AI 想跑破坏性命令、碰密钥、push 主分支 → 按 AGENTS.md 第四部分红线拒绝
4. **收工跑 evals**（见下节），全绿才算完成
5. **更新 tracker 再 commit**：WIP 表、决策日志（推翻的决策也留痕）、AI 协作上下文——这是下一个任务的输入

## 五、evals：AI 产出物的质量门禁

`04-Evals/regression-cases.json` 定义 13 个回归 case / 5 大类（代码质量、规范遵守、文档质量、AI 协作、安全合规），`runner.py` 自动化其中 3 个：

```bash
# 全量扫描，建立项目质量基线（首个结果就是你的基线）
python3 04-Evals/runner.py /path/to/你的代码仓库

# 增量模式：只检查最近 1 个 commit 的 message 规范（适合每次提交后跑）
python3 04-Evals/runner.py /path/to/你的代码仓库 --since HEAD~1
```

- **code-002**：应用代码无遗留调试残留（console.log / debugger / print / breakpoint；测试脚本与 CLI 工具自动豁免）
- **security-001**：无硬编码密钥 + 密钥文件未被 git 跟踪
- **spec-003**：commit message 符合 conventional commits + 首行 ≤72 字符

设计理念：**全量扫描的存量噪音不可怕，第一次跑出的就是"基线"**——之后增量守护新增，存量按告警清单渐进清零。历史 commit 不改写（代价大于收益），密钥全量审计交给 gitleaks / git-secrets 等专业工具。

## 六、角色分级：项目宪法只约束激活的角色

AGENTS.md 第二部分有「激活角色清单」，按 P0/P1/P2 三档管理：

| 档位 | 含义 | 示例 |
|---|---|---|
| **P0 常驻** | 项目装机即激活 | tech-lead / frontend / backend / qa / devops / orchestrator |
| **P1 阶段激活** | 进入对应阶段才拉起 | product-plan（需求/迭代）、ux-design（UI 改版）、data-analyst（埋点分析） |
| **P2 挂起** | 用不到就不写进宪法 | 按你的团队角色体系定义 |

**为什么这样设计**：规范越长，AI 遵守率越低。项目宪法只约束真正会拉起的角色，未激活角色不占上下文——这是宪法保持精简的关键机制。角色名完全按你的团队自定义，删改清单即可。

## 七、常见问题

**项目里有独立的子仓库（monorepo / 前后端分离）怎么办？**
install.sh 自动检测嵌套 git 仓库并写入根 .gitignore：根仓库管治理文件和文档，子仓库继续独立管理，互不污染。

**已装机的项目怎么升级模板？**
项目里的 AGENTS.md 会随项目实战演进（这是特性）。想拉齐新版模板：`git -C harness-kit pull` 后 diff 新旧模板手动挑选合并，合并后打 `harness-vX.Y` tag（约定见 AGENTS.md 附录 C）。

**怎么自定义 AI 能做/不能做的事？**
直接改项目根目录的 AGENTS.md：第三部分（白名单）、第四部分（红线）按项目风险等级调整。红线不要轻易删。

**evals 想加自己的 case？**
往 `regression-cases.json` 的对应 category 加 case（input / expected / check_method / rationale 四要素），自动化逻辑加进 runner.py。

## 八、设计原则

1. **Day1 版本控制 + 审计**：治理资产从第一天进 git，配置变更打 `harness-vX.Y` tag，可回滚
2. **最小特权**：白名单以外的工具，AI 调用前必须问人
3. **单一事实源**：任务状态只看 project-tracker.md，跨会话、跨 AI 角色共享
4. **0% 全自主起步**：默认"对话协作"档（AI 建议、人类全量 review），不追求 100% 自主
5. **模板单一来源**：仓库内的 02-规范 / 03-状态 是唯一模板源，install.sh 只引用不拷贝

## 九、目录结构

```
harness-kit/
├── 02-规范/AGENTS.md            # 项目宪法模板（10 部分 + 3 附录）
├── 02-规范/SECURITY.md          # 安全合规子法模板
├── 03-状态/project-tracker.md   # 状态持久化模板
├── 04-Evals/regression-cases.json  # 13 个回归 case / 5 类
├── 04-Evals/runner.py           # 最小 evals runner（v0.2）
└── 07-Kit/install.sh            # 一键装机脚本
```

## License

MIT
