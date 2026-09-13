# 05/06 Harness v1.5 迭代记录

## 结论

本次放弃维护 `09-ai-governance-example` 和 `10-ai-governance-kit-pro` 两个试验目录，回到 `05-Harness` / `06-harness-kit` 主线迭代。

原因：`05-Harness` 已经是母体工作台，`06-harness-kit` 已经是可分发 kit。继续维护新目录会制造第三套来源，增加漂移风险。

## 本次变更

1. 删除试验目录：
   - `09-ai-governance-example`
   - `10-ai-governance-kit-pro`
2. `06-harness-kit/07-Kit/install.sh` 升级到 v1.5：
   - 新增 `--with-local-skills`
   - 新增 `--skills-source`
   - 新增 `--with-adapters`
3. 新增 `05-Skills/README.md`：
   - 说明从 `日常办公/00-Skills汇总` 接入真实角色技能的规则
4. 新增 `06-Adapters/`：
   - `.claude/settings.json`
   - `.cursor/rules/harness.mdc`
   - `.github/copilot-instructions.md`
   - `.github/pull_request_template.md`
   - `.kiro/steering/harness.md`
5. `04-Evals/runner.py` 升级到 v0.3：
   - 新增 `harness-001`，检查 `AGENTS.md` / `project-tracker.md` / `SECURITY.md` 三件套是否落位
6. `05-Harness/06-工具链/harness-kit-sync-check.py` 扩展同步范围：
   - 新增检查 `05-Skills`
   - 新增检查 `06-Adapters`

## 装机命令

最小装机：

```bash
bash 06-harness-kit/07-Kit/install.sh /path/to/project
```

接入本地 Skills：

```bash
bash 06-harness-kit/07-Kit/install.sh /path/to/project --with-local-skills
```

接入本地 Skills + 多工具适配：

```bash
bash 06-harness-kit/07-Kit/install.sh /path/to/project --with-local-skills --with-adapters
```

## 验证结果

| 验证项 | 结果 |
|---|---|
| 删除 09/10 试验目录 | 已完成 |
| `06-harness-kit` 装机烟测 | 通过 |
| 本地 Skills 接入 | 通过，安装 16 个包含 `SKILL.md` 的技能 |
| 多工具适配安装 | 通过，生成 Claude / Cursor / GitHub Copilot / Kiro 配置 |
| evals runner v0.3 | 通过，4/4 pass |
| 05 ↔ 06 同步检查 | ALL CLEAR，待裁决 0 行 |

## 后续建议

下一步不要再开新目录，继续沿用：

```text
05-Harness      母体工作台
06-harness-kit  可分发 kit
08-ai-dev-suite 更完整的套件化方向
```

短期优先做 `doctor` 命令：在装机前检查目标项目是否已有 AGENTS、是否是 git 仓库、是否已有 skills、是否存在敏感文件风险。
