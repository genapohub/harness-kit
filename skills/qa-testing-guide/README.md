# QA Testing Guide — 测试 / QA 工程师方案产出指南

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](SKILL.md)

一个面向 AI 编程助手的 **测试 / QA 工程师 Skill**，将质量保障方法论转化为可执行工作流。自动识别 5 类场景（0→1 测试体系建设 / 中大型测试需求 / 单功能测试 / 测试策略升级 / 技术预研），按对应清单产出测试策略、自动化方案、性能压测方案、缺陷管理规范等完整交付物。

## 适用场景

| 场景 | 示例 | 产出量 |
|------|------|:---:|
| 0→1 测试体系建设 | 新项目全量测试基础设施 | 10-12类 |
| 中大型测试需求 | 新增模块全链路测试方案 | 6-8类 |
| 单功能测试/Bug验证 | 登录功能测试用例 | 2-3类 |
| 大版本测试策略升级 | 自动化覆盖率从30%→70% | 8-10类 |
| 测试技术预研 | 新工具评估、性能测试选型 | 3-4类 |

## 触发热词

测试、QA、测试策略、自动化测试、性能测试、压测、单元测试、集成测试、E2E测试、缺陷管理、质量保障、测试用例

---

## 安装

本 Skill 遵循 **Open Agent Skills 标准**（SKILL.md 格式），兼容以下工具：

### WorkBuddy / CodeBuddy

**方式一：克隆到 skills 目录**
```bash
git clone https://github.com/genapohub/qa-testing-guide.git ~/.workbuddy/skills/qa-testing-guide
```

### Trae

**ZIP 导入**
```bash
git clone https://github.com/genapohub/qa-testing-guide.git
zip -r qa-testing-guide.zip qa-testing-guide/
```
Trae → **设置** → **Rules & Skills** → **创建** → 上传 `qa-testing-guide.zip`。

### Codex / ZCode

```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/qa-testing-guide.git ~/.codex/skills/qa-testing-guide

# ZCode
git clone https://github.com/genapohub/qa-testing-guide.git ~/.zcode/skills/qa-testing-guide
```

重启 Codex / ZCode 客户端后自动发现。也可以在对话中输入 `$qa-testing-guide` 手动调用。

### Cursor
```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/qa-testing-guide.git ~/.cursor/skills-cursor/qa-testing-guide
```

重启 Cursor客户端 后自动发现。也可以在对话中输入 `$qa-testing-guide` 手动调用。

---


## 特性

- 5 类场景自动路由识别，产出清单按场景裁剪
- **内置可填空模板**：方法论内置「测试用例 / 性能测试场景」，产出时按占位符直接填充，文档规范度对齐业界标准

---

## 使用

```
帮我设计新项目的测试策略
用户模块的性能压测方案怎么出
搭建自动化测试框架，选什么工具
这个Bug的回归测试方案
```

## 许可

[MIT](LICENSE) © zhangmengbo
