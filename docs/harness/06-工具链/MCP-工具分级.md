# MCP 工具分级清单（L1~L5）

> **目的**：把当前 130+ 个 MCP/Connector 工具按风险分级，让 AI 调用有明确边界。
> **配套**：`06-工具链/工具治理白名单.md`（按角色分类）、`02-规范/SECURITY.md`（按数据敏感度分类），三件互补。
> **维护**：每次新增 MCP 工具，30 分钟内必须更新本文件。

---

## 一、一句话定位

**AI 调 MCP 不是无限制的游乐场，是有边界的工作车间。**

5 级风险模型（L1~L5 风险递增），每级对应明确的 AI 行为约束。

---

## 二、L1~L5 风险分级定义

| 级别 | 风险 | 性质 | AI 行为 |
|---|---|---|---|
| **L1 只读类** | 🟢 极低 | 数据查询 / 信息检索 / 文档读取 | ✅ **允许直接调用** |
| **L2 写入类** | 🟡 低 | 创建 / 编辑 / 上传（可逆） | ⚠️ **警告后调用**，留 audit log |
| **L3 破坏类** | 🟠 中 | 删除 / 修改 / 覆盖（部分可逆） | ⚠️ **必须人类授权**，留详细 audit log |
| **L4 外发类** | 🔴 高 | 对外发布 / 公开链接 / 推送到外部 | ❌ **禁止 AI 自动调用**，必须人类操作 |
| **L5 远程执行类** | 🔴🔴 极高 | SSH / 远程命令 / 自动化运维 / 数据库写 | 🚫 **完全禁止 AI 调用**，仅人类 DevOps/SRE |

---

## 三、按风险等级速查矩阵

### L1 只读类（AI 可直接调用）

**典型工具**：文档查询、信息检索、知识库搜索、行情数据查看、CRM 只读、邮件读取

| 工具类别 | 代表 MCP | 用途 |
|---|---|---|
| 知识库搜索 | lexiang / ima-mcp / kdocs / wps-knowledgebase / wk-workbuddy / fyopen-lawsearch / pkulaw / patsnap-search | 检索文档 |
| 文档读取 | tencent-docs (只读模式) / notion | 读用户文档 |
| 金融数据查询 | wind-finance / tushare / datayes-data / gildata / morningstar / westock-mcp / tdx-connector / dzh-mcp / mx-ds-mcp / gangtise-mcp / pandadata / efunds / yingmi-mcp / tongzhou-fin-research / proboost / qixinhuiyan-mcp / qcc-company / tyc-mcp | 查行情/财报/企业信息 |
| CRM 只读 | neo-crm / sharecrm / salestouch / salesnail-instructor | 查客户/订单 |
| 营销情报只读 | tec-do / chuhaijiang / youshu-bd-mate / fanruan-growth-advisor | 查行业情报 |
| HR 只读 | beisen-cli / gaodun-job / ihr-cli / moka / fenbi-baokao-decision / teacher-assistant | 查岗位/简历 |
| 数据 BI 只读 | jiushuyun / fanruan-growth-advisor | 查报表 |
| 财务只读 | yzf-general-mcp-server (只读模式) / lemonclaw / tplus-api (只读模式) | 查账 |
| 设计只读 | mastergo-vibe-mcp / canva / canva-ai | 读设计稿 |
| AI 模型只读 | alphapai-lite-mcp / ai-hive | 查模型信息 |
| 工具类只读 | textin-xparse / textin-xparse-ai / camscanner-mcp / today-watermark-camera | OCR / 解析 |
| 数据/地图只读 | opendata / tencent-map (只读模式) | 时空数据 / 地图 |

### L2 写入类（警告后调用，留 audit log）

**典型工具**：文档创建/编辑、消息发送、文件上传、本地数据库写、CRM 创建

| 工具类别 | 代表 MCP | 警告触发条件 |
|---|---|---|
| 文档写入 | tencent-docs (写入模式) / tencent-docs-oa / tencent-weiyun / kdocs / notion / kdocs / wps-knowledgebase | 写入生产文档时 |
| 邮件发送 | qq-mail / netease-mail | 发送外部邮件时 |
| CRM 写入 | neo-crm / sharecrm / salestouch | 创建/修改客户记录 |
| HR 写入 | beisen-cli / moka | 写入员工信息 |
| 财务写入 | yzf-general-mcp-server (写模式) / yzf-invoice-mcp-server | 开票/记账 |
| 文件上传 | baidu-netdisk / tencent-weiyun | 上传到云盘 |
| BI 数据写入 | jiushuyun / qingflow / lemonclaw | 写入报表数据 |
| 营销写入 | tec-do / youshu-bd-mate | 创建营销内容 |
| 设计写入 | mastergo-vibe-mcp / canva / canva-ai | 修改设计稿 |
| 低代码写入 | jiandaoyun / qingflow / h3yun-connector / shanlong-claw / xiaoe-cloud-cli / woscli / seeyon-office-marketing-suite | 创建/修改应用 |
| 教育写入 | teacher-assistant | 创建教学材料 |
| 项目管理写入 | tapd / linear-mcp / tanyuan-assistant | 创建任务 |
| 表单写入 | jinshuju / tencent-survey | 创建表单 |
| 视频/图像生成 | infimind-ecommerce-image / infimind-video / picset-commerce-images / picset-video-generation / kling-ai-plugin / kling-ai-plugin-ai | 生成图片/视频（高成本） |
| 营销广告写入 | tencentads / linkfox-product-selection | 创建广告 |
| 智能体邮箱 | agent-mail | 发送 AI 邮件（注意收件人） |

### L3 破坏类（必须人类授权）

**典型工具**：删除文件、覆盖配置、修改 CI/CD、删数据库记录

| 工具类别 | 代表 MCP | 必须人类授权原因 |
|---|---|---|
| 文件删除 | baidu-netdisk / tencent-weiyun / kdocs / notion | 删除可恢复但成本高 |
| 数据库修改 | tencent-dlc / emr-query / cloudbase / tencent-tchouse-c / dcs-cloud | 生产数据库写操作 |
| CI/CD 修改 | cnb-api / edgeone-pages | 部署流水线变更 |
| 营销系统修改 | tec-do / youshu-bd-mate / tencentads | 修改投放策略 |
| 设计系统修改 | mastergo-vibe-mcp / canva | 改设计系统组件 |

### L4 外发类（禁止 AI 自动调用）

**典型工具**：发布应用、生成分享链接、推送到社交媒体、发送付款请求、对外通知

| 工具类别 | 代表 MCP | 禁止原因 |
|---|---|---|
| 发布为应用 | edgeone-pages (publish) / sites | 发布动作一旦执行不可轻易撤回 |
| 微信支付 | weixinpay-pay / weixinpay-register / weixinpay-feedback | 涉及资金，必须人工 |
| 企微消息 | wecom / weisheng-scrm / salestouch | 涉及客户沟通 |
| 钉钉消息 | dingtalk | 涉及团队/客户沟通 |
| 飞书消息 | feishu | 涉及团队沟通 |
| 腾讯会议 | tmeet / ezjoin-meeting | 创建会议 |
| 邮件外发 | qq-mail / netease-mail (群发模式) | 群发不可撤回 |
| AI 客服 | tencent-qidian-cs | 直接面对客户 |
| 营销外发 | tiktok (发布视频) / lovrabet-cli / mglc / chuhaijiang | 公开内容发布 |
| 问卷推送 | tencent-survey | 群发问卷 |
| 公众号 | zsxq / xiaoe-cloud-cli | 内容平台发布 |
| 公益机构服务 | gongyi-open-mcp / dknowc-mcp / archive-hospital-mcp | 公开发布 |
| 跨境/出海 | proboost / linkfox-product-selection | 对外业务 |
| 远程协作 | awesun / tmeet | 创建连接 |
| 直播/视频 | kling-ai-plugin / infimind-video | 内容发布 |
| SaaS 应用发布 | miaoda / sites / edgeone-pages | 应用上线 |

### L5 远程执行类（完全禁止 AI 调用）

**典型工具**：SSH、远程命令、运维自动化、付款执行、数据库运维

| 工具类别 | 代表 MCP | 完全禁止原因 |
|---|---|---|
| 远程桌面 | awesun (远程控制) | 直接接管机器 |
| 数据库运维 | cloudbase / tencent-dlc (生产) / emr-query / tencent-tchouse-c | 不可逆操作 |
| 安全运维 | ioa / h3c-cloudnet | 涉及安全策略 |
| 法律/合规 | yuandian-mcp / fyopen-lawsearch (涉及诉讼) / pkulaw (诉讼) | 法律红线 |
| 医疗合规 | archive-hospital-mcp / tencent-health-nges | 医疗数据 |
| 信用/征信 | cisp-mcp / xingtu-claw-risk / mzl-trademark | 个人征信 |
| 资金操作 | weixinpay-pay (支付动作) / fbs-connector / fadada-richee (签章) | 资金红线 |
| 跑腿/物流 | uupt / shanlong-claw (餐饮) | 真实物理动作 |
| 票务/出行 | ctrip-wendao / tc-chengxin | 真实消费 |
| 公益 | gongyi-open-mcp | 公益资金 |
| HR 敏感操作 | beisen-cli (解雇) / moka (薪酬) | 人员红线 |

---

## 四、调用决策矩阵

```
L1 只读  → AI 直接调用 ✅
L2 写入  → AI 调用 + audit log ⚠️（人类 review audit）
L3 破坏  → AI 请求 → 人类授权 → AI 执行 ⚠️（必须留详细 log）
L4 外发  → AI 禁止调用，必须人类操作 ❌
L5 远程  → 完全禁止 AI 调用 🚫
```

**决策树伪代码**：

```python
def ai_can_call(tool, action):
    risk = tool.risk_level  # L1~L5
    if risk == "L1":
        return True, "audit log"
    elif risk == "L2":
        if action in tool.dangerous_actions:
            return False, "需要人类授权"
        return True, "audit log + review"
    elif risk == "L3":
        return False, "必须人类授权"
    elif risk in ("L4", "L5"):
        return False, "完全禁止"
```

---

## 五、AI 调用审计（强制要求）

所有 L2 以上的 MCP 调用必须留 audit log：

```yaml
audit_log 字段：
  - timestamp: ISO 8601 时间
  - ai_role: 调用方（哪个 SKILL.md）
  - tool_name: MCP 名
  - action: 具体动作
  - parameters: 参数（脱敏后）
  - risk_level: L1~L5
  - human_authorized: bool（是否有人类授权）
  - result: success/failure
  - error_message: 失败原因（如有）

存储位置：
  - 本地：`~/.workbuddy/audit/mcp-calls.jsonl`（每日一个文件）
  - 远程：密钥管理服务 + KMS 加密
  - 保留期：90 天
```

**审计原则**：

- L1 调用记录 7 天后可清理（量大）
- L2~L3 必须永久保留
- L4~L5 试图调用但被拒绝的尝试，也必须记录（防止越权试探）

---

## 六、新 MCP 接入 SOP

每接一个新的 MCP 工具，必须完成：

```markdown
- [ ] 工具名 + 用途记录到本文件
- [ ] 评估风险级别 L1~L5（参考本文档同类工具）
- [ ] 配置到对应角色 SKILL.md（参考 06-工具链/工具治理白名单.md）
- [ ] 写入 SECURITY.md 模型路由（如涉及数据敏感）
- [ ] 测试 AI 调用路径（手动验证 + 1 次自动验证）
- [ ] audit log 字段确认（至少含 6 个字段）
- [ ] 失败降级方案（如果 MCP 挂了，AI 怎么办）
```

**SLA 要求**：新 MCP 接入后 24 小时内必须完成上述清单。

---

## 七、MCP 退出 SOP

工具下线 / 不再使用时：

```markdown
- [ ] 从本文件删除（或标记 deprecated）
- [ ] 从对应角色 SKILL.md 移除调用方式
- [ ] audit log 历史记录保留 90 天后再清理
- [ ] 项目 README 更新（如有相关说明）
- [ ] 通知团队
```

---

## 八、Review Checklist

每次新增 MCP / 修改 MCP 配置的 PR：

```markdown
风险分级：
- [ ] 工具已分级 L1~L5（参考本文档第三部分）
- [ ] 分级理由已记录（为什么是这个级别）
- [ ] 同类工具分级一致（如 CRM 写入统一 L2）

调用规则：
- [ ] 写入类 L2 已配 audit log
- [ ] 破坏类 L3 已配人类授权机制
- [ ] 外发类 L4 已确认禁止 AI 调用
- [ ] 远程类 L5 已确认完全禁止

合规：
- [ ] 不涉及未成年人数据
- [ ] 不违反 SECURITY.md 模型路由
- [ ] 不违反 AGENTS.md 红线

审计：
- [ ] audit log 路径已配置
- [ ] 失败降级方案已测试
- [ ] 团队已通知新工具接入
```

---

## 九、关键决策速记

### 9.1 高频工具优先级

按使用频率和风险综合排序，前 10 名要严格管控：

| 排名 | 工具 | 风险 | 管控要点 |
|---|---|---|---|
| 1 | tencent-docs | L2/L4 | 写入配 audit，发布禁用 |
| 2 | github | L2/L3 | PR 创建 OK，merge/force push 禁用 |
| 3 | tencent-weiyun / baidu-netdisk | L2/L3 | 上传 OK，删除需授权 |
| 4 | lexiang / ima-mcp | L1 | 直接调用 |
| 5 | dingtalk / feishu / wecom | L4 | 完全禁用 AI 主动发消息 |
| 6 | mastergo-vibe-mcp | L2/L3 | 修改设计稿需授权 |
| 7 | edgeone-pages | L3/L4 | 部署需授权，发布禁用 |
| 8 | weixinpay-* | L5 | 完全禁用 |
| 9 | neo-crm / sharecrm | L2 | 创建/修改客户记录配 audit |
| 10 | wind-finance / tushare | L1 | 直接调用 |

### 9.2 高风险红线（绝对不可违反）

- ❌ 不让 AI 自动调用 weixinpay-pay（资金红线）
- ❌ 不让 AI 自动调用 feishu/dingtalk/wecom 发消息（沟通红线）
- ❌ 不让 AI 自动调用 edgeone-pages publish（发布红线）
- ❌ 不让 AI 调用 awesun 远程控制（机器红线）
- ❌ 不让 AI 调用 archive-hospital-mcp / tencent-health-nges（医疗红线）
- ❌ 不让 AI 调用 weixinpay-register 自动开通支付（合规红线）

### 9.3 灰色地带（按业务判断）

| 场景 | 判断 |
|---|---|
| AI 调用 kling-ai 生成视频 | ⚠️ 高成本，按配额控制 |
| AI 调用 infimind-ecommerce-image 生成电商图 | ⚠️ 中成本，可批量 |
| AI 调用 tencent-survey 推送问卷 | ❌ 推送动作人类操作，AI 只生成内容 |
| AI 调用 tushare 拉历史行情 | ✅ OK |
| AI 调用 patsnap-search 检索专利 | ✅ OK |
| AI 调用 tiktok 发布视频 | ❌ 必须人类操作 |

---

## 十、与三件套关系

```
SECURITY.md           → 按"数据敏感度"分类（密钥/脱敏/合规）
06-工具链/工具治理白名单.md → 按"角色"分类（13+1 角色允许/禁止）
MCP-工具分级.md（本文件） → 按"工具风险"分类（L1~L5 通用分级）

三件互补：
├── 决定能不能调（按工具风险）→ L1~L5
├── 决定谁有权调（按角色）→ 工具治理白名单
└── 决定能不能喂数据（按敏感度）→ SECURITY.md

决策路径：
  AI 想调用 MCP → 查本文件分级（L1~L5）
                → 查工具治理白名单（角色允许？）
                → 查 SECURITY.md（数据允许？）
                → 三关全过 → 执行 + audit
                → 任一关不过 → 拒绝 + 警告
```

---

## 附录 A：分级统计（截至 2026-09-05）

| 级别 | 数量 | 占比 |
|---|---|---|
| L1 只读类 | ~50 | ~38% |
| L2 写入类 | ~40 | ~31% |
| L3 破坏类 | ~10 | ~8% |
| L4 外发类 | ~20 | ~15% |
| L5 远程执行类 | ~12 | ~8% |
| **合计** | **~132** | **100%** |

> _统计来源：基于 WorkBuddy 当前可用 connector 列表，可能有 ±5 个误差_

---

> _维护原则：每接入新 MCP 必须更新，风险级别变更必须有理由记录。_
> _版本：v1.0（2026-09-05）· 由 05-Harness/06-工具链/MCP-工具分级.md 同步_
