# Harness v1.7 · 09 主线修正记录

## 结论

后续主线从 `06-harness-kit` 修正为 `09-ai-governance-example`。

新项目使用方式收敛为：

```bash
git clone git@github.com:genapohub/harness-kit.git your-project
```

克隆完成后，`your-project/` 就是项目根目录，不再要求执行任何装机命令。

## 修正原因

用户明确要求：

1. 不要把额外脚本作为装机步骤。
2. `08-ai-dev-suite` 应该与 `09` 融合后迭代 `09`，以后直接维护 `09`。

## 执行结果

1. `06-harness-kit` 当前直接克隆模板已迁移为 `09-ai-governance-example`。
2. README 已改为“一步 clone 到项目根目录”。
3. `AGENTS.md` 已新增 `harness-v1.7` 版本记录。
4. `scripts/` 仅作为维护工具保留，不作为新项目启动必需步骤。

## 风险说明

此前 `08-ai-dev-suite` 与旧 `09-ai-governance-example` 已按上一轮指令物理删除，本地搜索未找到可恢复原始目录。当前 v1.7 是基于已合并 05 沉淀、本地 Skills 和多工具适配后的模板重建 09 主线。

后续如需把 08 原始内容补回，需要从 GitHub、备份、压缩包或其它机器恢复原始 `08-ai-dev-suite`。
