# b2b-need-mining-guide

AI Agent Skill：B端企业客户需求挖掘全流程助手，双模式。①输入公司信息（名称/行业/规模/组织结构/业务描述/客户群体），自动生成四层角色（老板/中层/执行/IT）定制访谈问题库；②输入访谈素材（录音转写/笔记），自动加工出岗位任务清单、三维打分、算账、P0/P1 需求清单与交付账单。兼容 WorkBuddy / Codex / Trae / Cursor。

## 核心能力

### 模式一：访谈问题库生成（拜访前）

- **输入公司信息 → 输出可打印的访谈问题库**：按行业推断岗位地图，按角色生成 8-10 问（60% 基础问题 + 40% 嵌入公司业务的定制问题）
- **四层角色分层提问**：老板问钱和效率 / 中层问管理卡点 / 执行层问重复劳动 / IT 问集成
- **高潜痛点预判**：行业 × 岗位 × 痛点 × 产品线（AI客服/AI名片/品牌推流/AI内部管理）映射

### 模式二：访谈后加工（24 小时内）

- **输入访谈素材 → 输出需求清单与交付账单**：素材整理成事件卡片 → 岗位任务清单 → 三维打分（频次×耗时×出错，≥10 进高潜池）→ 算账 → 预判校准 → P0/P1 清单 + 账单 + 交接说明
- **内置算账引擎**：年化成本 = 频次 × 耗时 × 时薪 × 250天 + 出错损失，支撑报价与 ROI 谈判
- **红线自检**：不问卷、不第一轮讲参数、不听信单方、不承诺全定制、不当天逼单、不谈价、账单不覆盖 P2+

## 触发方式

**模式一（拜访前）**——说"生成访谈问题库 / 准备客户拜访 / 挖需求"并提供企业信息，例如：

> 帮我生成访谈问题库：郑州一家 30 人的外贸公司，主营家居出口，客户是欧美采购商，老板姓赵，组织结构有销售 12 人、客服 4 人、运营 6 人、财务 3 人。

**模式二（访谈后）**——说"整理访谈记录 / 加工访谈 / 出需求清单和账单"并提供访谈素材，例如：

> 帮我整理今天的访谈记录：嘉和木业赵总说客服人力吃紧，客服主管说每人每天回 150-250 条消息，凌晨询盘没人接，上季度丢过 2 个大客户损失约 15 万……

## 安装

本 Skill 遵循 **Open Agent Skills 标准**（SKILL.md 格式），兼容以下工具：

### WorkBuddy / CodeBuddy

**方式一：克隆到 skills 目录**
```bash
git clone https://github.com/genapohub/b2b-need-mining-guide.git ~/.workbuddy/skills/b2b-need-mining-guide
```

**方式二：ZIP导入**
```bash
git clone https://github.com/genapohub/b2b-need-mining-guide.git
zip -r b2b-need-mining-guide.zip b2b-need-mining-guide/
```
然后在 WorkBuddy 桌面端 → **技能市场** → **添加技能/上传技能** → **点击"跳过检测，直接安装"**。

### Trae

**ZIP 导入**
```bash
git clone https://github.com/genapohub/b2b-need-mining-guide.git
```
然后在 Trae → **设置** → **Rules & Skills** → **创建** → 上传 `b2b-need-mining-guide.zip`。

### Codex / ZCode

```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/b2b-need-mining-guide.git ~/.codex/skills/b2b-need-mining-guide

# ZCode
git clone https://github.com/genapohub/b2b-need-mining-guide.git ~/.zcode/skills/b2b-need-mining-guide
```

重启 Codex / ZCode 客户端后自动发现。也可以在对话中输入 `${b2b-need-mining-guide}` 手动调用。

### Cursor
```bash
# 克隆到 skills 目录
git clone https://github.com/genapohub/b2b-need-mining-guide.git ~/.cursor/skills-cursor/b2b-need-mining-guide
```

重启 Cursor客户端 后自动发现。也可以在对话中输入 `${b2b-need-mining-guide}` 手动调用。

## 目录结构

```
b2b-need-mining-guide/
├── SKILL.md                      # 主流程：信息收集 → 岗位地图 → 问题库生成 → 痛点预判
├── references/
│   ├── question-bank.md          # 四层角色基础问题库 + 控场技巧
│   ├── industry-map.md           # 行业×岗位×痛点×产品线映射 + 规模分级策略
│   └── templates.md              # 任务清单/算账公式/优先级表/需求卡片模板
├── README.md
└── LICENSE
```

## License

MIT © zhangmengbo
