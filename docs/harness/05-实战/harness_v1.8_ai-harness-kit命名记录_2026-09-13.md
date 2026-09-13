# harness v1.8 · ai-harness-kit 命名记录

> 日期：2026-09-13
> 结论：后续通用 AI 编程治理模板统一命名为 `ai-harness-kit`。

## 一、调整结论

1. 本地维护目录从 `ai-governance-example` 更名为 `ai-harness-kit`。
2. 远程仓库目标从 `genapohub/harness-kit` 更名为 `genapohub/ai-harness-kit`。
3. 对外克隆入口统一为：

```bash
git clone git@github.com:genapohub/ai-harness-kit.git your-project
```

## 二、命名原因

`ai-governance-example` 更像一个示例项目名，容易让使用者误解为参考样例。

`ai-harness-kit` 更准确表达当前定位：

1. `ai`：面向 AI 编程协作。
2. `harness`：提供项目级约束、状态、技能、evals、工具适配的治理框架。
3. `kit`：可直接克隆、可作为 GitHub Template 复用。

## 三、同步范围

本次需要同步的当前入口：

1. `README.md`：标题、维护主线、克隆地址、版本说明。
2. `AGENTS.md`：版本记录与底部版本号。
3. `project-tracker.md`：Harness 版本、版本日志、底部版本号。
4. `SECURITY.md`：底部版本号。
5. `evals/regression-cases.json`：回归基线创建方与项目名。
6. Git remote：`git@github.com:genapohub/ai-harness-kit.git`。

## 四、历史口径

`docs/harness/` 中 v1.5、v1.6、v1.7 文件保留当时的历史判断，不做全量抹改。后续维护以 v1.8 为准。

---

> _版本：v1.8（2026-09-13）· ai-harness-kit_
