# Harness v1.6 单仓库合并记录

## 结论

`05-Harness` 与 `06-harness-kit` 合并为直接克隆模板。后续主线已在 v1.7 修正为 `09-ai-governance-example`。

合并后的模板不再是“装机脚本仓库”，而是 GitHub 可直接克隆的项目根目录模板。

## 为什么合并

原结构的优点是职责清晰：

- `05-Harness`：母体工作台，存调研、实战、工具链。
- `06-harness-kit`：可分发 kit，给项目装机。

但长期使用会有三个问题：

1. 双源维护成本高，每次改规则都要同步。
2. 装机路径太长，新项目启动不够顺手。
3. Skills 和 Adapters 还要靠参数安装，不如直接成为项目根能力。

## 合并方式

1. `05-Harness/01-调研` 迁入 `docs/harness/01-调研`。
2. `05-Harness/05-实战` 迁入 `docs/harness/05-实战`。
3. `05-Harness/06-工具链` 迁入 `docs/harness/06-工具链`。
4. `06-harness-kit/02-规范` 提升为根目录 `AGENTS.md` / `SECURITY.md`。
5. `06-harness-kit/03-状态` 提升为根目录 `project-tracker.md`。
6. `06-harness-kit/04-Evals` 提升为根目录 `evals/`。
7. `06-harness-kit/06-Adapters` 提升为根目录 `.claude` / `.cursor` / `.github` / `.kiro`。
8. 本地 `00-Skills汇总` 同步为根目录 `skills/`。

## 新项目使用方式

推荐 GitHub Template：

```bash
git clone git@github.com:genapohub/harness-kit.git your-project
cd your-project
git remote rename origin harness-template
git remote add origin git@github.com:your-org/your-project.git
```

更推荐在 GitHub 页面使用 Template repository 创建业务仓库，这样不需要手动调整 `origin`。

## 验证结果

| 项目 | 结果 |
|---|---|
| `08-ai-dev-suite` 删除 | 已完成 |
| `05-Harness` 合并进 `06-harness-kit` | 已完成 |
| 根目录三件套 | 已落位 |
| 本地 Skills | 已内置 16 个 |
| 多工具适配 | 已内置 Claude / Cursor / GitHub Copilot / Kiro |
| evals runner | v0.3，4 项检查 |

## 后续维护原则

1. 不再恢复 `05-Harness` / `06-harness-kit` / `08-ai-dev-suite` 分叉目录。
2. 后续只在 `09-ai-governance-example` 修改规则、技能、evals、适配文件。
3. 每次治理规则变更都更新 `AGENTS.md` 版本段。
4. 每次稳定变更都打 `harness-vX.Y` tag。
