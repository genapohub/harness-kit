# ai-harness-kit · AI 编程 Harness 项目根模板

> 后续主线维护仓库：`ai-harness-kit`。
> 目标是一件事：从 GitHub 克隆下来，目录本身就是项目根目录，不再额外执行装机脚本。

## 一、怎么用

### 新项目

```bash
git clone git@github.com:genapohub/ai-harness-kit.git your-project
```

克隆完成后，`your-project/` 就已经是带 AI 编程治理能力的项目根目录。

如果这是你的业务项目仓库，进入目录后把远端改成业务仓库：

```bash
cd your-project
git remote rename origin governance-template
git remote add origin git@github.com:your-org/your-project.git
```

更推荐在 GitHub 上把本仓库设置为 Template repository。以后新项目直接从模板创建，连改远端这一步都省掉。

### 已有项目

已有项目如果已经有 `.git`，不要把本仓库直接 clone 到里面。推荐两种方式：

1. 用 GitHub Template 创建新仓库，再迁移业务代码。
2. 从本仓库复制治理资产到已有项目根目录。

## 二、克隆后自带什么

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
├── skills/                    # 本地角色技能库，默认内置 16 个技能
├── evals/                     # AI 产出质量回归检查
├── scripts/                   # 维护脚本，日常使用无需先执行
└── docs/harness/              # 05 沉淀 + ai-harness-kit 主线迭代记录
```

## 三、克隆后只需要改三处

1. `AGENTS.md`：项目目标、目标用户、技术栈、当前阶段。
2. `project-tracker.md`：当前阶段总览、WIP、风险、决策日志。
3. `.ai/SKILLS.md`：确认本项目启用哪些角色技能。

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

当前版本：`harness-v1.8`

v1.8 变更：

1. 本地与远程仓库统一命名为 `ai-harness-kit`。
2. 克隆地址切换为 `git@github.com:genapohub/ai-harness-kit.git`。
3. README、AGENTS、project-tracker、SECURITY、evals 元信息统一更换为新名称。

v1.7 变更：

1. 后续维护主线当时切到 `ai-governance-example`，v1.8 已统一更名为 `ai-harness-kit`。
2. 使用方式收敛为“直接克隆到项目根目录”，不再要求执行装机命令。
3. README 去掉克隆后的自检命令，把脚本降为维护工具。
4. 标记 08 原始目录待备份恢复后再补融合。

v1.6 变更：

1. 合并 `05-Harness` 母体资料到 `docs/harness/`。
2. 仓库升级为可直接克隆的项目根目录模板。
3. 默认内置本地角色技能和多工具适配文件。

## 六、维护原则

1. 以后只维护 `ai-harness-kit`。
2. 不再保留 `05-Harness` / `06-harness-kit` 多套分叉；`08-ai-dev-suite` 原始内容待备份恢复后补入 `ai-harness-kit`。
3. 新项目优先用 GitHub Template 创建。
4. 规则、技能、evals、适配文件都跟项目根目录一起进入版本控制。
5. 每次稳定变更都更新 `AGENTS.md` 版本段，并打 `harness-vX.Y` tag。
