# Team Orchestrator — 虚拟科技公司调度指挥官

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-green.svg)](SKILL.md)

一个面向 AI 编程助手的 **调度指挥官 Skill**，管理 13 个专业 AI 角色组成的虚拟研发团队。自动分析用户意图、按需调度角色、串联上下文、追踪项目进度——一句话即可驱动全流程。

## 能力

- **智能路由**：根据用户输入自动匹配需要的角色，不必要的一个不多调
- **三种模式**：全流程跑通 / 按需组合 / 增量补充
- **上下文串联**：角色产出自动传递，无需重复交代项目背景
- **进度追踪**：记忆系统记录项目阶段和关键决策

## 管理的 13 个角色

| 角色 | Skill | 典型产出 |
|------|-------|---------|
| 产品经理 | product-plan-guide | PRD/BRD/MRD |
| 技术负责人 | tech-lead-guide | 架构设计/ADR |
| 项目管理 | project-mgmt-guide | WBS/里程碑/风险 |
| UI/UX设计师 | ui-designer-guide | 交互方案/视觉执行/设计系统/设计转代码 |
| 平面设计师 | graphic-design-guide | 品牌VI/视觉资产 |
| 前端开发 | frontend-dev-guide | 组件方案/前端架构 |
| 后端开发 | backend-dev-guide | API设计/数据库 |
| 测试/QA | qa-testing-guide | 测试策略/自动化 |
| DevOps/运维 | devops-guide | CI/CD/K8s |
| 数据分析 | data-analyst-guide | 指标体系/BI看板 |
| 增长负责人 | growth-guide | 增长模型/获客矩阵 |
| 商业化负责人 | monetization-guide | 定价/销售漏斗 |
| 运营经理 | operations-guide | 用户生命周期/内容 |

## 触发热词

从0到上线、全流程、完整方案、端到端、调度、团队协作、整个项目、研发团队、虚拟团队

---

## 安装

本 Skill 遵循 **Open Agent Skills 标准**（SKILL.md 格式），兼容以下工具：

### WorkBuddy / CodeBuddy

**方式一：克隆到 skills 目录**
```bash
git clone https://github.com/genapohub/team-orchestrator.git ~/.workbuddy/skills/team-orchestrator
```

### Trae

**ZIP 导入**
```bash
git clone https://github.com/genapohub/team-orchestrator.git
zip -r team-orchestrator.zip team-orchestrator/
```
然后在 Trae → **设置** → **Rules & Skills** → **创建** → 上传 `team-orchestrator.zip`。

### Codex / ZCode

```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/team-orchestrator.git ~/.codex/skills/team-orchestrator

# ZCode
git clone https://github.com/genapohub/team-orchestrator.git ~/.zcode/skills/team-orchestrator
```

重启 Codex / ZCode 客户端后自动发现。也可以在对话中输入 `$team-orchestrator` 手动调用。

### Cursor
```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/team-orchestrator.git ~/.cursor/skills-cursor/team-orchestrator
```

重启 Cursor客户端 后自动发现。也可以在对话中输入 `$team-orchestrator` 手动调用。

---

## 使用

```
从0到上线做一个宠物托运小程序
用户流失严重，出增长+运营+数据分析的组合方案
上次PRD基础上补个埋点和技术选型方案
给我的SaaS产品做完整的商业化方案
```

Skill 会自动分析意图，匹配需要的角色，按依赖关系编排执行。

## 灵活调用机制

指挥官可灵活调度 13 个角色 Skill，**无需全部安装**——只安装你需要的即可：

- 指挥官在调度每个角色前，会自动检测该 Skill 是否已本地安装（检查 `~/.workbuddy/skills/`、`~/.codex/skills/`、`~/.cursor/skills-cursor/` 等路径）
- 若目标 Skill 已安装 → 正常调度执行，自动串联上下文
- 若目标 Skill 未安装 → 指挥官暂停并提示：

```
检测到 {角色名}（{skill-name}）未安装，调度无法继续。

安装方式：
git clone https://github.com/genapohub/{skill-name}.git ~/.workbuddy/skills/{skill-name}

是否确认安装后继续？
```

- 确认安装后继续执行；拒绝则自动跳过该角色，不影响其余调度
- 被调度的角色可同时独立使用——在对话中直接 `$角色名` 即可，历史记忆互通

## 许可

[MIT](LICENSE) © zhangmengbo
