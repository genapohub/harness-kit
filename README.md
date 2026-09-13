# harness-kit · 可直接克隆的 AI 编程治理项目模板

> 这是一个 GitHub 模板仓库形态的 Harness：克隆后，项目根目录天然带 `AGENTS.md`、`project-tracker.md`、`SECURITY.md`、`skills/`、`evals/` 和多 AI 工具适配文件。

## 一、推荐用法

### 新项目

推荐在 GitHub 上把本仓库设置为 Template repository，然后用模板创建你的业务仓库。这样新仓库的 `origin` 天然就是业务仓库，不会指回 harness-kit。

如果直接 clone：

```bash
git clone git@github.com:genapohub/harness-kit.git your-project
cd your-project
git remote rename origin harness-template
git remote add origin git@github.com:your-org/your-project.git
```

然后补齐：

1. `AGENTS.md` 第一部分：项目目标、目标用户、技术栈、当前阶段。
2. `project-tracker.md` 当前阶段总览、WIP、风险、决策日志。
3. `.ai/SKILLS.md`：确认本项目真正启用哪些角色技能。

### 已有项目

已有项目不建议直接把 Git 仓库 clone 到根目录，容易和现有 `.git` 冲突。建议用 GitHub 模板开新仓库后迁移业务代码，或手动复制本仓库中的治理资产：

```text
AGENTS.md
project-tracker.md
SECURITY.md
.ai/
.claude/
.cursor/
.github/
.kiro/
skills/
evals/
docs/harness/
scripts/
```

## 二、目录结构

```text
your-project/
├── AGENTS.md                  # AI 行为宪法：项目身份、角色、红线、工作流
├── project-tracker.md         # 项目状态单一事实源：WIP、风险、决策、AI 交接
├── SECURITY.md                # 安全子法：密钥、脱敏、模型路由、事故响应
├── .ai/SKILLS.md              # 项目技能索引
├── .claude/settings.json      # Claude Code 权限建议
├── .cursor/rules/harness.mdc  # Cursor 项目规则
├── .github/                   # Copilot 指令 + PR 模板
├── .kiro/steering/harness.md  # Kiro steering
├── skills/                    # 从本地 00-Skills汇总 同步来的角色技能
├── evals/                     # AI 产出质量回归检查
├── scripts/                   # 本地检查 / 技能刷新脚本
└── docs/harness/              # 05-Harness 历史调研、实战、工具链沉淀
```

## 三、日常命令

运行 Harness 自检：

```bash
bash scripts/harness-check.sh
```

刷新本地 Skills：

```bash
bash scripts/refresh-skills.sh /Users/macos/Downloads/WorkBuddy/日常办公/00-Skills汇总
```

直接跑 evals：

```bash
python3 evals/runner.py .
python3 evals/runner.py . --since HEAD~1
```

## 四、默认能力

| 能力 | 文件 |
|---|---|
| AI 行为规范 | `AGENTS.md` |
| 项目状态持久化 | `project-tracker.md` |
| 安全红线 | `SECURITY.md` |
| 本地角色技能 | `skills/` + `.ai/SKILLS.md` |
| Claude Code 适配 | `.claude/settings.json` |
| Cursor 适配 | `.cursor/rules/harness.mdc` |
| GitHub Copilot 适配 | `.github/copilot-instructions.md` |
| PR 模板 | `.github/pull_request_template.md` |
| Kiro 适配 | `.kiro/steering/harness.md` |
| 质量回归检查 | `evals/runner.py` |
| 历史沉淀 | `docs/harness/` |

## 五、版本

当前版本：`harness-v1.6`

v1.6 变更：

1. 合并 `05-Harness` 母体资料到 `docs/harness/`。
2. 删除 05/08 分叉方向，后续只维护 `06-harness-kit`。
3. 仓库升级为可直接克隆的项目根目录模板。
4. 默认内置本地角色技能和多工具适配文件。

## 六、原则

1. 新项目优先用 GitHub Template，不再跑安装脚本。
2. 已有项目谨慎直接 clone，避免覆盖现有 Git 仓库。
3. 治理资产进入项目第一天就进版本控制。
4. Skills 不再散落在外部目录，项目根目录自带可读技能索引。
5. 任何 Harness 规则变更都要更新 `AGENTS.md` 版本段，并打 `harness-vX.Y` tag。
