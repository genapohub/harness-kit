#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能库自检脚本 (skill-library-selfcheck.py)
============================================
对 01-Skills技能指南 全部技能仓库做一键健康检查（蒸馏/改版后必跑）。

检查维度：
  1. 仓库完整性      —— 目录齐全、git 存在、无未提交变更
  2. frontmatter     —— SKILL.md name 与目录一致、version 存在
  3. 引用指向        —— SKILL.md 里 references/*.md 引用是否指向真实文件
  4. expert-distill  —— 蒸馏文档结构（来源标注 + 蒸馏记录尾行）
  5. 副本一致性      —— 源仓库 vs WorkBuddy 副本(~/.workbuddy/skills) MD5
  6. remote 纪律     —— 所有 remote 必须 SSH（防 HTTPS 静默失败）
  7. GitHub 同步     —— 源仓库本地 HEAD vs origin/main 是否一致（领先=未推送）

用法：
  python3 skill-library-selfcheck.py            # 默认检查技能指南目录
  python3 skill-library-selfcheck.py <路径>     # 指定技能目录

退出码：0 = 全绿；1 = 有问题
"""

import os, re, sys, glob, hashlib, subprocess

DEFAULT = "/Users/macos/Downloads/WorkBuddy/日常办公/01-Skills技能指南"
ROOT = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
COPY = os.path.expanduser("~/.workbuddy/skills")

issues, mismatches = [], []
OK = "\033[32m✔\033[0m"; BAD = "\033[31m✘\033[0m"

def git(repo, *args):
    try:
        return subprocess.run(["git", "-C", repo, *args], capture_output=True,
                              text=True, timeout=30).stdout.strip()
    except Exception:
        return ""

repos = sorted([d for d in glob.glob(ROOT + "/*") if os.path.isdir(d)
                and os.path.isdir(os.path.join(d, ".git"))])
print(f"检查目录: {ROOT}")
print(f"技能仓库数: {len(repos)}\n")

# 1. 仓库完整性 + git clean
print("=== 1. 仓库完整性 / git clean ===")
for d in repos:
    n = os.path.basename(d)
    if not os.path.exists(os.path.join(d, "SKILL.md")): issues.append(f"{n}: 缺 SKILL.md")
    dirty = git(d, "status", "--porcelain")
    if dirty: issues.append(f"{n}: {len(dirty.splitlines())} 个未提交变更")
print(f"{OK if not issues else BAD} 完成")

# 2. frontmatter
print("=== 2. frontmatter（name 一致 / version 存在）===")
bad = 0
for d in repos:
    n = os.path.basename(d)
    lines = open(os.path.join(d, "SKILL.md"), encoding="utf-8").read(2000).splitlines()
    name_ok = len(lines) > 1 and lines[1].strip() == f"name: {n}"
    ver_ok = any(l.startswith("version:") for l in lines[:15])
    if not (name_ok and ver_ok):
        bad += 1; issues.append(f"{n}: frontmatter 异常 (name_ok={name_ok}, ver_ok={ver_ok})")
print(f"{OK if bad == 0 else BAD} {len(repos) - bad}/{len(repos)}")

# 3. 引用指向
print("=== 3. SKILL.md 引用指向 ===")
bad = 0
for d in repos:
    n = os.path.basename(d)
    txt = open(os.path.join(d, "SKILL.md"), encoding="utf-8").read()
    refs = set(re.findall(r"`(references/[A-Za-z0-9_./\-\u4e00-\u9fff]+\.md)`", txt))
    refs |= set(re.findall(r"(references/expert-distill/[A-Za-z0-9_./\-\u4e00-\u9fff]+)", txt))
    for r in sorted(refs):
        if not os.path.exists(os.path.join(d, r)):
            bad += 1; issues.append(f"{n}: 引用缺失 {r}")
print(f"{OK if bad == 0 else BAD} 缺失 {bad}")

# 4. expert-distill 结构
print("=== 4. expert-distill 蒸馏结构 ===")
total, bad = 0, 0
for d in repos:
    n = os.path.basename(d)
    ed = os.path.join(d, "references/expert-distill")
    if not os.path.isdir(ed): continue
    for f in sorted(glob.glob(ed + "/*.md")):
        total += 1
        t = open(f, encoding="utf-8").read()
        if not ("来源" in t and "蒸馏" in t): bad += 1; issues.append(f"{n}/{os.path.basename(f)}: 缺来源")
        if "蒸馏记录" not in t: bad += 1; issues.append(f"{n}/{os.path.basename(f)}: 缺蒸馏记录尾行")
print(f"{OK if bad == 0 else BAD} 蒸馏文档 {total} 份，结构异常 {bad}")

# 5. 源 vs WorkBuddy 副本 MD5
print("=== 5. 源仓库 vs WorkBuddy 副本 MD5 ===")
bad = 0
for d in repos:
    n = os.path.basename(d)
    wd = os.path.join(COPY, n)
    if not os.path.isdir(wd): mismatches.append(f"{n}: 副本不存在"); bad += 1; continue
    for root, _, fnames in os.walk(d):
        if ".git" in root: continue
        for fn in fnames:
            sf = os.path.join(root, fn)
            rel = os.path.relpath(sf, d)
            wf = os.path.join(wd, rel)
            if not os.path.exists(wf): mismatches.append(f"{n}: 副本缺 {rel}"); bad += 1; continue
            if hashlib.md5(open(sf, "rb").read()).hexdigest() != hashlib.md5(open(wf, "rb").read()).hexdigest():
                mismatches.append(f"{n}: 不一致 {rel}"); bad += 1
print(f"{OK if bad == 0 else BAD} 不一致 {bad}")
for m in mismatches[:15]: print(f"  {BAD} {m}")

# 6. remote 纪律（必须 SSH）
print("=== 6. remote 类型（必须 SSH）===")
bad = 0
for d in repos:
    n = os.path.basename(d)
    u = git(d, "remote", "get-url", "origin")
    if u and not u.startswith("git@"):
        bad += 1; issues.append(f"{n}: HTTPS remote → {u}（需改 SSH）")
print(f"{OK if bad == 0 else BAD} {len(repos) - bad}/{len(repos)} SSH")

# 7. GitHub 同步（本地 vs origin/main）
print("=== 7. GitHub 同步状态（领先=未推送）===")
bad = 0
for d in repos:
    n = os.path.basename(d)
    local = git(d, "rev-parse", "HEAD")
    remote = git(d, "rev-parse", "origin/main")
    if local and remote and local != remote:
        bad += 1; issues.append(f"{n}: 未推送（本地 {local[:7]} vs 远端 {remote[:7]}）")
print(f"{OK if bad == 0 else BAD} 领先 {bad} 个仓库（0 = 全部已推送）")

# 汇总
print("\n" + "=" * 50)
print(f"汇总：蒸馏 {total} 份 | 问题 {len(issues) + len(mismatches)} 项")
for i in issues[:20]: print(f"  {BAD} {i}")
if not issues and not mismatches:
    print("ALL GREEN ✅")
    sys.exit(0)
print("存在需修复项，见上 ⚠️")
sys.exit(1)
