# Python 全栈工程师专家蒸馏 · Python Full-Stack Engineer（深网网同源）

> **来源**：WorkBuddy 专家中心「Python 全栈工程师」专家包蒸馏（2026-09-06）
> **源包**：`~/.workbuddy/plugins/marketplaces/experts/plugins/python-fullstack-engineer/agents/python-fullstack-engineer.md`（95 行）
> **蒸馏方式**：方法论精华提炼，并入 backend-dev-guide 的 expert-distill，作为 Python 生态纵深增量。
> **定位**：本地 `后端开发方法论.md` 讲通用后端方案（5 场景产出清单），本文档补 **Python 技术栈选型、分层工程模板、工程质量基线**。

---

## 一、Python 技术栈选型速查表

> 后端方案涉及 Python 生态时，直接按表定选型，避免"调研三天"。

| 场景 | 首选方案 | 备选 |
|------|----------|------|
| REST API | FastAPI + Pydantic v2 | Django REST Framework |
| 全栈 Web | Django + HTMX | FastAPI + Jinja2 |
| 数据分析 | Pandas + Polars + Plotly | NumPy + Matplotlib |
| 机器学习 | scikit-learn → PyTorch | TensorFlow/Keras |
| 自动化脚本 | pathlib + schedule + typer | APScheduler |
| 浏览器自动化 | Playwright (async) | Selenium |
| 爬虫 | httpx + parsel（轻量） | Scrapy（大规模） |
| CLI 工具 | Typer | Click |
| 测试 | pytest + hypothesis | unittest |
| 包管理 | uv | Poetry |
| 代码质量 | Ruff（lint+format 一体） | Black + isort + flake8 |
| 配置 | pydantic-settings | django-environ |

**选型逻辑**：每个场景给"首选 + 备选"而非唯一答案——首选满足 80% 场景，遇到约束（团队熟悉度/遗留系统/部署环境）降级到备选不慌。

---

## 二、Python 服务端标准分层模板（工程骨架）

> 给 Python 后端项目立目录时直接套此模板，职责清晰、可测、可演进。

```
project-name/
├── src/app/
│   ├── main.py          # 入口（FastAPI app）
│   ├── config.py        # pydantic-settings 配置
│   ├── dependencies.py  # FastAPI 依赖注入
│   ├── models/          # SQLAlchemy ORM 模型
│   ├── schemas/         # Pydantic request/response
│   ├── services/        # 业务逻辑层
│   ├── repositories/    # 数据访问层
│   ├── api/v1/          # 路由（版本化）
│   └── utils/
├── tests/               # conftest.py + test_api/ + test_services/
├── pyproject.toml       # 项目配置 + 依赖
├── Dockerfile / docker-compose.yml / Makefile
├── .env.example
└── README.md
```

**分层纪律**（依赖方向单向，禁止倒流）：
```
api (路由) → services (业务) → repositories (数据) → models/schemas
utils 任何层可调；models/schemas 不许反向依赖上层
```
- 路由层**不做业务逻辑**，只做参数校验 + 调 service
- services 层**不直接碰 DB**，走 repositories——换 DB/加缓存不动业务代码
- 所有跨层传参用 schema（Pydantic），不用 dict 裸奔

---

## 三、Python 代码质量基线

1. **函数签名标准**：类型注解 + docstring（`Args / Returns / Raises` 三段齐全）——不是可选，是作业标准
2. **注释写"为什么"**：解释设计取舍，不解释"做了什么"（做了什么代码自己会说）
3. **测试**：pytest + hypothesis（属性测试补边界）；核心业务 ≥ 80% 覆盖
4. **工具链**：uv 管包、Ruff 管 lint+format、pre-commit 门禁
5. **工程规范**：pyproject.toml 集中配置；类型检查跑 mypy（或 pyright）进 CI

---

## 四、Python 工程师红线（输出物自检）

- 不碰生产环境的数据库和密钥，除非用户明确授权
- 不执行未经验证的第三方脚本
- 不外泄任何私密数据
- 不擅自运行破坏性命令：**优先 `trash` 而非 `rm`**（可恢复优于永久删除）；破坏性操作前先询问
- 遇到不确定的安全问题，先问再做

---

## 五、代码输出规范（给 AI 产出代码的验收标准）

- [ ] 代码完整可运行：含所有 import，可直接复制运行
- [ ] 附带依赖说明：`pyproject.toml` 片段或 `pip install` / `uv add` 命令
- [ ] 关键逻辑加"为什么"注释（不是"做了什么"）
- [ ] 主动指出潜在的坑与优化方向（至少 1 条）
- [ ] 给出运行命令：`uv run python main.py` 或 `uvicorn app.main:app --reload`
- [ ] 函数签名类型注解 + docstring 齐全

---

## 六、首响路由（接到需求先判断场景）

```
是 Web 后端/API？→ 查本文档一（REST API 行）+ 后端开发方法论对应场景
是全栈 Web 页面？→ Django + HTMX 优先
是数据分析/报表？→ Pandas/Polars + Plotly
是 ML 模型接入？→ scikit-learn → PyTorch
是自动化/爬虫？→ 脚本用 schedule+typer / 爬虫用 httpx 或 Scrapy
```

---

## 七、与原生方法论的配合

| 场景 | 用哪个 |
|------|--------|
| 5 场景识别 / 方案产出清单 / 交付衔接 | `后端开发方法论.md`（原生，主） |
| 通用后端技术选型（语言/框架/DB 横向对比） | 原生方法论技术选型章节 |
| **Python 生态具体选型 / 分层模板 / 质量基线** | **本文档（增量，唯一来源）** |

> **使用原则**：先读原生方法论定位场景产出清单，进入代码设计阶段后用本文档定 Python 技术栈、套分层模板、按输出规范验收。

---

_蒸馏记录：v1.0（2026-09-06）· 专家「Python 全栈工程师」→ backend-dev-guide/expert-distill/_
