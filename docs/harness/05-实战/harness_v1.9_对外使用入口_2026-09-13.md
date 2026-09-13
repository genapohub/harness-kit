# harness v1.9 · 对外使用入口记录

> 日期：2026-09-13
> 结论：`ai-harness-kit` 的对外使用方式收敛为 GitHub Template 优先、直接克隆补充、已有项目复制治理资产。

## 一、对外用户主路径

### 新项目

优先使用 GitHub Template：

1. 打开 `https://github.com/genapohub/ai-harness-kit`。
2. 点击 `Use this template`。
3. 创建自己的业务项目仓库。
4. 克隆业务仓库到本地。
5. 修改 `AGENTS.md`、`project-tracker.md`、`.ai/SKILLS.md` 三个入口文件。

### 直接克隆

适合不使用 GitHub Template 的用户：

```bash
git clone https://github.com/genapohub/ai-harness-kit.git your-project
cd your-project
git remote rename origin ai-harness-kit-template
git remote add origin git@github.com:your-org/your-project.git
```

### 已有项目

已有项目不要嵌套 clone。复制以下治理资产到项目根目录：

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
```

## 二、本次调整

1. README 重写为对外用户使用版。
2. 明确三条路径：Template、Clone、已有项目复制。
3. 增加不同 AI 工具读取规则。
4. 增加质量检查说明。
5. GitHub 仓库开启 Template repository。

## 三、验收标准

1. 仓库公开可访问。
2. GitHub `is_template=true`。
3. README 第一屏能让外部用户判断自己该走哪条路径。
4. `master` 和 `harness-v1.9` 均推送到远程。

---

> _版本：v1.9（2026-09-13）· ai-harness-kit_
