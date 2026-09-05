# 07-Kit · Harness 一条命令装机

把 Harness 治理三件套装进目标项目根目录，替代手动复制。

## 用法

```bash
bash install.sh /path/to/项目
```

## 脚本自动完成

| 动作 | 说明 |
|---|---|
| 三件套落位 | AGENTS.md / project-tracker.md / SECURITY.md → 项目根目录 |
| 占位符填充 | 项目名、日期、责任人、P0 激活角色（6 个）自动填入 |
| 路径断链修复 | 模板里指向本仓库的相对引用改写为你机器上的绝对路径 |
| 嵌套仓库隔离 | 项目内的独立 git 仓库（如 04-前后端代码/xxx）自动加入 .gitignore，代码仓库继续独立管理 |
| Day1 版本控制 | git init（main 分支）+ 初始 commit + `harness-vX.Y` tag |

## 约定

- 模板直接引用 `02-规范/`、`03-状态/` 原件，**本目录不持有模板拷贝**（单一事实源）
- 防覆盖：目标项目已有 AGENTS.md 时中止
- `HARNESS_VERSION` 变量与 AGENTS.md 版本号同步维护，升级模板时改这一处
- 装机后手工待办见脚本输出（项目身份 YAML / P1 角色勾选 / tracker 阶段总览）
