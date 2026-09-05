#!/usr/bin/env python3
"""Harness 最小 evals runner · v0.2

对应 regression-cases.json 中可自动化的 3 个 case:
  code-002     无遗留调试代码（console.log / debugger / print( / breakpoint）
  security-001 无密钥泄露（硬编码密钥模式 + .env 被 git 跟踪）
  spec-003     commit message 规范（conventional commits 前缀 + 首行长度）

用法:
  python3 runner.py /path/to/repo                     # 终端摘要 + JSON 报告落盘
  python3 runner.py /path/to/repo --since HEAD~1      # spec-003 增量模式: 只查最近 1 个 commit

v0.2 变更（来自真实项目首扫实战反馈）:
  - code-002 豁免 test_*.py / deploy/ / migrate_* / scripts/ —— 测试与 CLI 脚本的
    print 输出是设计意图，不是遗留调试代码
  - security-001 修两类假阳性: .env.example 属合法跟踪文件；密钥正则收紧为赋值形式
    （不再跨行、不再误报 os.getenv 读取模式）
  - spec-003 支持 --since 增量模式（历史存量 commit 不改写，用增量守护新增）

v0.1 边界仍适用:
  - 全量扫描存量代码会产生噪音，首个结果作为「质量基线」
  - 历史全量密钥审计交给 gitleaks 等专业工具
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Optional

RUNNER_VERSION = "0.2"

CODE_EXTS = {".py", ".js", ".ts", ".vue", ".wxml", ".json"}
SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__",
             ".miniprogram_npm", "venv", ".venv", "logs", "data"}
COMMIT_SAMPLE = 10

# code-002 豁免清单: 路径/文件名以此为前缀的文件不参与调试残留检查
DEBUG_EXEMPT = ("test_", "deploy/", "migrate_", "scripts/")

# code-002 调试残留模式（按语言分组）
DEBUG_PATTERNS = {
    ".py": [r"\bprint\(", r"\bbreakpoint\(", r"pdb\.set_trace\("],
    ".js": [r"console\.log\(", r"\bdebugger\b"],
    ".ts": [r"console\.log\(", r"\bdebugger\b"],
    ".vue": [r"console\.log\(", r"\bdebugger\b"],
    ".wxml": [],
    ".json": [],
}

# security-001 硬编码密钥模式（name, regex）
SECRET_PATTERNS = [
    ("wechat_appsecret", r"[Aa]pp[Ss]ecret\W{0,5}([a-f0-9]{32})"),
    ("openai_key", r"sk-[A-Za-z0-9_\-]{20,}"),
    ("aws_access_key", r"AKIA[0-9A-Z]{16}"),
    ("github_token", r"ghp_[A-Za-z0-9]{30,}"),
    ("generic_password", r"""(?i)\b(password|passwd|pwd)\s*=\s*['"][^'"\n]{4,}['"]"""),
    ("generic_api_key", r"""(?i)\b(api[_-]?key|secret[_-]?key)\s*=\s*['"][A-Za-z0-9_\-]{16,}['"]"""),
]

CONVENTIONAL_RE = re.compile(
    r"^(feat|fix|refactor|docs|test|chore|style|perf|build|ci)(\([^)]*\))?: \S")


def list_code_files(repo: Path):
    for p in sorted(repo.rglob("*")):
        if not p.is_file() or p.suffix not in CODE_EXTS:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        yield p


def git(repo: Path, *args) -> str:
    out = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else ""


def scan_debug(repo: Path):
    """code-002: 应用代码中的遗留调试代码（测试脚本/CLI 工具/迁移脚本豁免）"""
    hits = []
    for p in list_code_files(repo):
        rel = str(p.relative_to(repo))
        if rel.startswith(DEBUG_EXEMPT):
            continue
        pats = DEBUG_PATTERNS.get(p.suffix, [])
        if not pats:
            continue
        try:
            for i, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
                for pat in pats:
                    if re.search(pat, line):
                        hits.append({"file": rel, "line": i,
                                     "match": line.strip()[:80]})
                        break
        except OSError:
            continue
    return hits


def scan_secrets(repo: Path):
    """security-001: 硬编码密钥 + .env 被 git 跟踪"""
    hits = []
    for p in list_code_files(repo):
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        for name, pat in SECRET_PATTERNS:
            for m in re.finditer(pat, text):
                line_no = text.count("\n", 0, m.start()) + 1
                line = text.splitlines()[line_no - 1]
                if "getenv" in line or "environ[" in line:
                    continue  # 从环境读取密钥的合法模式
                hits.append({"file": str(p.relative_to(repo)), "line": line_no,
                             "type": name, "match": m.group(0)[:60]})
    tracked = [f for f in git(repo, "ls-files").splitlines()
               if f == ".env" or (f.startswith(".env.") and "example" not in f)]
    for f in tracked:
        hits.append({"file": f, "line": 0, "type": "env_file_tracked",
                     "match": "密钥文件被 git 跟踪（应 gitignore + git rm --cached，若已进历史需轮换）"})
    return hits


def scan_commits(repo: Path, since: Optional[str] = None):
    """spec-003: commit message 规范（默认最近 N 条；--since 后只查 <since>..HEAD）"""
    rng = [f"{since}..HEAD"] if since else [f"-{COMMIT_SAMPLE}"]
    hits = []
    log = git(repo, "log", *rng, "--pretty=%h %s").strip()
    for line in log.splitlines():
        if not line:
            continue
        sha, subject = line.split(" ", 1)
        if not CONVENTIONAL_RE.match(subject):
            hits.append({"commit": sha, "issue": "缺 conventional 前缀", "subject": subject[:80]})
        elif len(subject) > 72:
            hits.append({"commit": sha, "issue": f"首行 {len(subject)} 字符 > 72", "subject": subject[:80]})
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", help="目标 git 仓库路径")
    ap.add_argument("--json", dest="json_out", default=None, help="JSON 报告输出路径")
    ap.add_argument("--since", default=None,
                    help="spec-003 增量模式: 只检查 <since>..HEAD（如 HEAD~1）")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        sys.exit(f"❌ 目录不存在: {repo}")

    cases = [
        {"id": "code-002", "name": "无遗留调试代码", "hits": scan_debug(repo)},
        {"id": "security-001", "name": "无密钥泄露", "hits": scan_secrets(repo)},
        {"id": "spec-003", "name": "commit message 规范", "hits": scan_commits(repo, args.since)},
    ]
    for c in cases:
        c["status"] = "pass" if not c["hits"] else "fail"

    report = {
        "repo": repo.name, "date": date.today().isoformat(),
        "runner": RUNNER_VERSION,
        "summary": {"pass": sum(1 for c in cases if c["status"] == "pass"),
                    "fail": sum(1 for c in cases if c["status"] == "fail")},
        "cases": cases,
    }

    print(f"\n=== evals 基线 · {repo.name} · runner v{RUNNER_VERSION} ===")
    for c in cases:
        mark = "✅" if c["status"] == "pass" else "❌"
        print(f"{mark} {c['id']} {c['name']}: {len(c['hits'])} 处命中")
        for h in c["hits"][:10]:
            loc = h.get("file", h.get("commit", "?"))
            line = f":{h['line']}" if h.get("line") else ""
            detail = h.get("match") or h.get("subject") or h.get("issue", "")
            print(f"     {loc}{line}  {h.get('type', h.get('issue', ''))}  {detail}")
        if len(c["hits"]) > 10:
            print(f"     … 其余 {len(c['hits']) - 10} 处见 JSON 报告")
    passed = report["summary"]["pass"]
    print(f"--- 结果: {passed}/3 pass" + ("（基线已建立，建议按告警清单整改后复跑）" if passed < 3 else "，全绿") + "\n")

    out = Path(args.json_out) if args.json_out else \
        Path(__file__).parent / "reports" / f"{date.today().isoformat()}-{repo.name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"📄 报告: {out}")

    sys.exit(0 if report["summary"]["fail"] == 0 else 1)


if __name__ == "__main__":
    main()
