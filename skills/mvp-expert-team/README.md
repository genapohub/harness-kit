# MVP 开发专家团 — mvp-expert-team

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](SKILL.md)

一个面向 AI 编程助手的 **MVP 端到端交付专家团 Skill**——项目总监统筹 7 位领域专家（产品经理 / 首席架构师 / UI设计师 / 前端工程师 / 后端工程师 / 测试工程师 / 运维工程师），一句话想法 → 可运行 MVP。阶段门禁 + 团队级 P0 反 AI 规则，自包含、不依赖任何其他 Skill。

## 能力

- **六阶段门禁流水线**：需求澄清 → 三文档调研 → 用户确认 → Spec 规格契约锁定（12 章）→ 设计细化 → 并行开发 + 自检 → 测试归零 → 部署交付，每阶段有产出物 + 门禁，不跳步
- **团队级 P0 三红线**：禁 emoji 作功能图标 / 禁紫→粉渐变主视觉 / 禁 AI 模板味（空洞占位、硬编码色、千篇一律 Hero）——每道门禁强制执行
- **机器可读契约**：openapi.yaml + design-tokens.json 作为放行门槛，反 AI 味从设计层落到代码层
- **测试反作弊门**：先写测试（写测试的 ≠ 写代码的）+ 5 类作弊检测 + P0 缺陷归零才上线
- **两种执行模式**：多代理编排（子代理并行）/ 单代理角色切换（换视角自审），产出与门禁一致

## 团队构成（自包含 7 角色）

| 角色 | 文件 | 职责 |
|------|------|------|
| 产品经理 | `agents/01-产品经理-pm.md` | 需求挖掘、竞品调研（差评找空白）、RICE 排序、PRD |
| 首席架构师 | `agents/02-首席架构师-architect.md` | 技术选型对比矩阵、API/DB 契约、ADR、可行性验证 |
| UI设计师 | `agents/03-UI设计师-designer.md` | 寄存器判断、反 AI 模板主职、四层 Token、DESIGN.md |
| 前端工程师 | `agents/04-前端工程师-frontend.md` | 设计不过反模式检查不写代码、自检循环、19 项视觉检查 |
| 后端工程师 | `agents/05-后端工程师-backend.md` | 分层架构、错误三层、安全清单、失效模式 6 类自检 |
| 测试工程师 | `agents/06-测试工程师-qa.md` | 先写测试、反作弊门、回归集沉淀、生产就绪评级 |
| 运维工程师 | `agents/07-运维工程师-devops.md` | 部署可回滚、健康检查、备份、自包含交付包 |

## 触发热词

做成MVP、从零开发、一句话变产品、帮我做个产品、端到端交付、全栈实现、需求到上线、完整产品开发、MVP开发

---

## 安装

本 Skill 遵循 **Open Agent Skills 标准**（SKILL.md 格式），兼容以下工具：

### WorkBuddy / CodeBuddy

**方式一：克隆到 skills 目录**
```bash
git clone https://github.com/genapohub/mvp-expert-team.git ~/.workbuddy/skills/mvp-expert-team
```

**方式二：ZIP导入**
```bash
git clone https://github.com/genapohub/mvp-expert-team.git
zip -r mvp-expert-team.zip mvp-expert-team/
```
然后在 WorkBuddy 桌面端 → **技能市场** → **添加技能/上传技能** → **点击"跳过检测，直接安装"**。

### Trae

**ZIP 导入**
```bash
git clone https://github.com/genapohub/mvp-expert-team.git
```
然后在 Trae → **设置** → **Rules & Skills** → **创建** → 上传 `mvp-expert-team.zip`。

### Codex / ZCode

```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/mvp-expert-team.git ~/.codex/skills/mvp-expert-team

# ZCode
git clone https://github.com/genapohub/mvp-expert-team.git ~/.zcode/skills/mvp-expert-team
```

重启 Codex / ZCode 客户端后自动发现。也可以在对话中输入 `$mvp-expert-team` 手动调用。

### Cursor
```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/mvp-expert-team.git ~/.cursor/skills-cursor/mvp-expert-team
```

重启 Cursor客户端 后自动发现。也可以在对话中输入 `$mvp-expert-team` 手动调用。

---

## 仓库结构

```
mvp-expert-team/
├── SKILL.md                     # 项目总监主控：定位/P0红线/快速路径/执行模式/6阶段/角色索引/门禁
├── README.md                    # 本文件
├── LICENSE                      # MIT
├── .gitignore
├── agents/                      # 7 个角色独立文件（各含完整方法论与模板）
│   ├── 01-产品经理-pm.md
│   ├── 02-首席架构师-architect.md
│   ├── 03-UI设计师-designer.md
│   ├── 04-前端工程师-frontend.md
│   ├── 05-后端工程师-backend.md
│   ├── 06-测试工程师-qa.md
│   └── 07-运维工程师-devops.md
├── memory/                      # 技能记忆区（每次调用先读后写，随技能携带）
│   ├── README.md                # 记忆目录说明
│   ├── MEMORY.md                # 长期记忆：可复用决策/用户偏好
│   ├── project-tracker.md       # 项目进度台账：里程碑/裁决
│   ├── YYYY-MM-DD.md            # 活跃日志（运行时追加）
│   └── archive/                 # 月度归档
└── references/                  # 团队共享知识库
    ├── 01-全流程模板库.md       # PRD/Spec/OpenAPI/ADR/DESIGN/质量报告等可填空模板
    ├── 02-P0规则与反AI清单.md   # 红线细规 + 7大罪 + 12禁令 + 19项视觉检查 + AI痕迹检测
    ├── 03-工程纪律与自检.md     # 代码组织/失效模式6类/测试反作弊/记分卡/门禁汇总
    └── 04-记忆规则.md           # memory/ 生命周期：读写时机/日志格式/轮转归档算法
```

## 使用

**触发**：说出想法 → 自动以项目总监身份启动 → 6 阶段流水线

```
[一句话想法]
    ↓
Phase 0 需求澄清（主控提问 check list，3 句话确认）
    ↓
Phase 1 并行调研（PM竞品 + 架构选型 + 设计方向 三文档并行）
    ↓ 【唯一必扰交互点：用户确认三文档】
Phase 1.5 Spec 锁定（12 章规格契约，从此以 Spec 为唯一依据）
    ↓
Phase 2 设计细化（openapi.yaml + design-tokens.json 机器可读契约）
    ↓ 【P0 扫描 + 反模式检查 + emoji 扫描】
Phase 3 并行开发（前端 + 后端按 Spec 实现 + 自检链 lint→type→test）
    ↓ 【代码组织门禁 + emoji 扫描 + 视觉检查 + 联调】
Phase 4 测试交付（QA 反作弊门 + P0 归零 → 运维部署 → 交付包）
    ↓
[可运行 MVP + 自包含交付包 + 完整文档 + 7×3 评级 ≥ Silver]
```

**使用示例**：

```
我想从零做一个团队协作工具，做成 MVP
帮我开发一个电商小程序
把这个宠物托运的想法做成能上线的产品
```

主控按快速路径判断（轻量/标准/迷你）激活角色范围，逐 Phase 门禁推进。

## 来源与致谢

本技能承载 WorkBuddy「MVP开发专家团」专家包 v2.1.0（大湾区靓仔 × 7 专家团队）的完整方法论，2026-09-06 整理为独立技能。工程纪律部分源自该专家包内嵌的 UmaDev 知识库方法论（MIT License，详见 `references/03-工程纪律与自检.md`）。内容剔除多 Agent 环境专属机制（Team spawn / SendMessage / IMA MCP），适配多代理与单代理两种执行模式。

## 许可

[MIT](LICENSE) © zhangmengbo
