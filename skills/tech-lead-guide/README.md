# Tech Lead Guide — 技术负责人 / 架构师方案产出指南

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](SKILL.md)

一个面向 AI 编程助手的 **技术负责人 / 架构师 Skill**，将架构决策方法论转化为可执行工作流。自动识别 5 类场景（0→1 技术体系搭建 / 技术决策改造 / 单点评审 / 架构演进 / 战略规划），按对应清单产出架构设计、技术选型方案、ADR、技术债务治理方案等完整交付物。

## 适用场景

| 场景 | 示例 | 产出量 |
|------|------|:---:|
| 0→1 技术体系搭建 | 全新产品线全栈技术定义 | 10-12类 |
| 中型技术决策/改造 | 前端框架选型、模块重构 | 6-8类 |
| 单点决策/技术评审 | 缓存方案评审、ADR记录 | 2-3类 |
| 大版本架构演进 | 单体→微服务、遗留系统现代化 | 8-10类 |
| 技术预研/战略规划 | 技术雷达更新、新技术评估 | 3-4类 |

## 触发热词

架构、技术选型、技术债务、系统设计、架构演进、ADR、技术决策、技术负责人、架构师

---

## 安装

本 Skill 遵循 **Open Agent Skills 标准**（SKILL.md 格式），兼容以下工具：

### WorkBuddy / CodeBuddy

**方式一：克隆到 skills 目录**
```bash
git clone https://github.com/genapohub/tech-lead-guide.git ~/.workbuddy/skills/tech-lead-guide
```

### Trae

**ZIP 导入**
```bash
git clone https://github.com/genapohub/tech-lead-guide.git
zip -r tech-lead-guide.zip tech-lead-guide/
```
Trae → **设置** → **Rules & Skills** → **创建** → 上传 `tech-lead-guide.zip`。

### Codex / ZCode

```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/tech-lead-guide.git ~/.codex/skills/tech-lead-guide

# ZCode
git clone https://github.com/genapohub/tech-lead-guide.git ~/.zcode/skills/tech-lead-guide
```

重启 Codex / ZCode 客户端后自动发现。也可以在对话中输入 `$tech-lead-guide` 手动调用。

### Cursor
```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/tech-lead-guide.git ~/.cursor/skills-cursor/tech-lead-guide
```

重启 Cursor客户端 后自动发现。也可以在对话中输入 `$tech-lead-guide` 手动调用。

---


## 特性

- 5 类场景自动路由识别，产出清单按场景裁剪
- **内置可填空模板**：方法论内置「技术选型评估（配套 ADR 决策记录）」，产出时按占位符直接填充，文档规范度对齐业界标准

---

## 使用

```
帮我做新项目的全栈技术选型
这个架构方案帮我把把关
单体应用拆微服务，怎么渐进式演进
技术债务太多，帮我出个治理方案
```

## 许可

[MIT](LICENSE) © zhangmengbo
