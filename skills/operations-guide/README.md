# Operations Guide — 运营经理方案产出指南

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](SKILL.md)

一个面向 AI 编程助手的 **运营经理 Skill**，将运营方法论转化为可执行工作流。自动识别 5 类场景（0→1 运营体系搭建 / 中大型运营活动 / 小任务日常运营 / 运营体系升级 / 运营策略研究），按对应清单产出用户生命周期策略、内容矩阵、活动方案、客服SLA等完整交付物。

## 适用场景

| 场景 | 示例 | 产出量 |
|------|------|:---:|
| 0→1 运营体系搭建 | 新产品上线全链路运营基础设施 | 10-12类 |
| 中大型运营活动 | 节日Campaign、年度盛典、拉新促活 | 6-8类 |
| 小任务/日常运营 | 单次Push、单篇文章、社群维护 | 2-3类 |
| 运营体系升级 | 运营工具替换、私域体系搭建 | 8-10类 |
| 运营策略研究 | 竞品运营策略分析、新渠道评估 | 3-4类 |

## 触发热词

运营、活动运营、内容运营、用户运营、社区运营、客户成功、客服、触达、Push、私域、CRM、用户生命周期

---

## 安装

本 Skill 遵循 **Open Agent Skills 标准**（SKILL.md 格式），兼容以下工具：

### WorkBuddy / CodeBuddy

**方式一：克隆到 skills 目录**
```bash
git clone https://github.com/genapohub/operations-guide.git ~/.workbuddy/skills/operations-guide
```

### Trae

**ZIP 导入**
```bash
git clone https://github.com/genapohub/operations-guide.git
zip -r operations-guide.zip operations-guide/
```
然后在 Trae → **设置** → **Rules & Skills** → **创建** → 上传 `operations-guide.zip`。

### Codex / ZCode

```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/operations-guide.git ~/.codex/skills/operations-guide

# ZCode
git clone https://github.com/genapohub/operations-guide.git ~/.zcode/skills/operations-guide
```

重启 Codex / ZCode 客户端后自动发现。也可以在对话中输入 `$operations-guide` 手动调用。

### Cursor
```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/operations-guide.git ~/.cursor/skills-cursor/operations-guide
```

重启 Cursor客户端 后自动发现。也可以在对话中输入 `$operations-guide` 手动调用。

---


## 特性

- 5 类场景自动路由识别，产出清单按场景裁剪
- **内置可填空模板**：方法论内置「活动策划 SOP」，产出时按占位符直接填充，文档规范度对齐业界标准

---

## 使用

```
帮我搭建产品的用户运营体系
做个双11的活动策划方案
设计新用户激活的Onboarding流程
用户流失严重，出个挽回方案
```

## 许可

[MIT](LICENSE) © zhangmengbo
