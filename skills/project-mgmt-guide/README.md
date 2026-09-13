# Project Management Guide — 项目管理方案产出指南

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](SKILL.md)

一个面向 AI 编程助手的 **项目管理 Skill**，将项目管理方法论转化为可执行工作流。自动识别 5 类场景（0→1 项目启动 / 迭代版本规划 / 问题跟进 / 项目重启 / 流程优化），按对应清单产出项目章程、WBS、里程碑排期、风险登记册、沟通计划等完整交付物。

## 适用场景

| 场景 | 示例 | 产出量 |
|------|------|:---:|
| 0→1 项目启动 | 全新产品立项规划 | 10-12类 |
| 中型迭代/版本规划 | V1.2 版本 Sprint 规划 | 6-8类 |
| 小调整/问题跟进 | 资源调整、单事项跟进 | 2-3类 |
| 项目重启/重大调整 | 项目暂停后重启、范围变更 | 8-10类 |
| 敏捷转型/流程优化 | Scrum 导入、流程改进 | 3-4类 |

## 触发热词

项目管理、迭代规划、项目计划、WBS、里程碑、风险管理、Sprint、进度跟踪、复盘、敏捷、Scrum

---

## 安装

本 Skill 遵循 **Open Agent Skills 标准**（SKILL.md 格式），兼容以下工具：

### WorkBuddy / CodeBuddy

**方式一：克隆到 skills 目录**
```bash
git clone https://github.com/genapohub/project-mgmt-guide.git ~/.workbuddy/skills/project-mgmt-guide
```

### Trae

**ZIP 导入**
```bash
git clone https://github.com/genapohub/project-mgmt-guide.git
zip -r project-mgmt-guide.zip project-mgmt-guide/
```
Trae → **设置** → **Rules & Skills** → **创建** → 上传 `project-mgmt-guide.zip`。

### Codex / ZCode

```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/project-mgmt-guide.git ~/.codex/skills/project-mgmt-guide

# ZCode
git clone https://github.com/genapohub/project-mgmt-guide.git ~/.zcode/skills/project-mgmt-guide
```

重启 Codex / ZCode 客户端后自动发现。也可以在对话中输入 `$project-mgmt-guide` 手动调用。

### Cursor
```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/project-mgmt-guide.git ~/.cursor/skills-cursor/project-mgmt-guide
```

重启 Cursor客户端 后自动发现。也可以在对话中输入 `$project-mgmt-guide` 手动调用。

---


## 特性

- 5 类场景自动路由识别，产出清单按场景裁剪
- **内置可填空模板**：方法论内置「项目计划 WBS / 风险登记册」，产出时按占位符直接填充，文档规范度对齐业界标准

---

## 使用

```
帮我做新产品的项目启动规划
下个Sprint的迭代计划怎么排
这个项目的风险有哪些，怎么应对
项目复盘，总结下经验教训
```

## 许可

[MIT](LICENSE) © zhangmengbo
