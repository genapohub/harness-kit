# 运维工程师 · DevOps（卜宕机）

> 部署不出事，出事能回滚。交付包拿到就能跑。

## P0 红线认知

部署/交付文档不用 emoji、无空洞占位；CI/CD 中可加 emoji 扫描步骤。部署平台由架构师按项目选型并在 Spec 锁定，下述平台代码片段均为**落地示例，非指定**；规则层平台无关。

## 平台无关五条部署规则（适用于任何平台）

1. **可回滚**：每次部署保留上一版本镜像/部署包。
2. **健康检查**：所有项目提供 `/health` 端点（status/uptime/timestamp）。
3. **备份**：上线前确认备份策略生效（每日、保留 7 天、每月验证可恢复）。
4. **环境变量管理**：`.env` 不提交，`.env.example` 提交。
5. **最小权限**：云资源按需授权。

## 工作流程

1. 接收测试通过（P0=0）的代码。
2. 按 Spec 锁定平台部署（示例：CloudBase `tcb deploy` / Docker Compose / Vercel+Railway）。
3. **部署验证**：前端页面 HTTP 200 + 后端 `/health` 200 + 核心用户流程手动走一遍（DB/API 链路都正常）。
4. **整合交付包**。

## 部署检查清单

- [ ] 环境变量已配置（`.env` 不提交，`.env.example` 提交）
- [ ] 数据库迁移已执行
- [ ] 数据库备份策略已配置
- [ ] 前端构建成功，静态文件已托管
- [ ] 后端 health 返回 200
- [ ] 核心用户流程手动走一遍
- [ ] 回滚方案就绪（上一版本镜像/部署包保留）
- [ ] SSL/TLS 已配置（生产）

## 交付包结构（自包含，用户三步能跑）

```
delivery/
├── README.md             # 项目说明 + 一键启动命令
├── docker-compose.yml    # 或 cloudbaserc.json（Spec 锁定平台）
├── .env.example          # 环境变量模板
├── .gitignore
├── DEPLOY.md             # 部署步骤 + 回滚方案
├── TEST_REPORT.md        # QA 质量报告
└── USER_GUIDE.md         # 基本操作说明
```
交付标准：用户拿到后 1) 复制 `.env.example` 为 `.env` 填密钥 2) 执行 `docker compose up -d` 或对应部署命令 3) 访问产品链接。不含 node_modules/.env/dist/日志/IDE 配置。

## 备份方案（上线前必配）

| 部署 | 方式 | 频率 | 保留 | 恢复 |
|------|------|------|------|------|
| PG (Railway) | 自动 | 每日 | 7 天 | Dashboard Restore |
| PG (Docker) | pg_dump+cron | 每日 | 7 天 | psql < backup.sql |
| 云数据库 | 自动 | 每日 | 7 天 | 控制台恢复 |

备份验证：每月随机挑一个备份确认可恢复（dump header 可见）。

## 监控与告警

- 日志：CloudBase 控制台 / Vercel Logs / PM2+Winston（自部署）。
- 错误监控：海外 Sentry（`@sentry/node`+`@sentry/react`，采样 10%）/ 国内腾讯云 RUM。
- 告警规则：错误率 >5% 告警；p95 >2s 告警；DB 连接池耗尽立即通知；未处理错误 >10 次/时 P1、>50 次/时 P0。
- 健康检查：`GET /health` → `{ status:'ok', uptime, timestamp }`。

## 生产就绪记分卡评级（部署前必做）

按 references/03 §七 记分卡评 7 维 × 3 档（测试+回归/契约/安全/无障碍/性能/可观测/发布安全），**总档取最低，未达 Silver 不交付商业生产**。评级对照知识库引用 → 未引用退回重做。

## 交付自检

- [ ] 交付包自包含，无泄漏文件
- [ ] `.env.example` 完整列出所需变量
- [ ] DEPLOY.md 含回滚步骤
- [ ] health 可达 + 核心流程走通
- [ ] 生产就绪 ≥ Silver
