#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harness-kit-sync-check.py · 05-Harness(母体) ↔ 06-harness-kit(分发) 模板对齐核查

05-Harness 与 06-harness-kit 是"双源"关系：
  05 = 母体工作台（含私有件引用：06-工具链/05-实战/01-调研/四端同步），模板在此演进；
  06 = 可分发子集（不含私有件，内容做通用化 + 去隐私改写）。
模板大改后需人工把增量"通用化改写"后搬进 kit —— 本脚本一键出差异报告，
自动归类"预期分化"（差异属于设计，无需同步），只把"待裁决行"聚拢给人眼扫。

两层检查:
  A. 文件级（结构性）：动态扫描 4 个模板目录，05 与 kit 文件清单不一致 → 必报警
     （覆盖"新增模板文件漏同步"——即使 changelog 里伪装也逃不掉）
  B. 内容级（逐文件 diff）自动归类，规则按优先级:
     1. 特征行    A 侧命中母体定制特征 / B 侧命中分发通用特征 → 预期分化
     2. changelog "- " 开头 / git tag 行 → 两侧各自维护版本历史，不要求一致
     3. 目录树行  ├──/└── 且文件名为已知模板 → 描述性排版差异（新文件名会漏出报警）
     4. 伴随行    仅结构噪音行（空行/代码围栏/闭合符）且 ±4 行内有命中行 → 上下文伴随
                 （有实质内容的行绝不靠邻域归类，防真漂移被误吞）
     5. 其余      → 待裁决（真漂移候选，需人工看）

用法:
  python3 harness-kit-sync-check.py [A_dir] [B_dir]
  默认 A_dir = <脚本>/../.. 下的 05-Harness，B_dir = 同级 06-harness-kit

退出码:
  0 = 结构完整（无文件级漂移）；待裁决行已打印（可能有 0~n 行需人工裁决）
  1 = 文件级漂移：模板目录文件清单两侧不一致（先补齐/确认再谈内容）
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
A_DEFAULT = os.path.join(ROOT, "05-Harness")
B_DEFAULT = os.path.join(ROOT, "06-harness-kit")

# kit 可分发子集 = 这 6 个模板目录（05 的 01-调研/05-实战/06-工具链 是母体私有件，不在比对范围）
TEMPLATE_DIRS = ["02-规范", "03-状态", "04-Evals", "05-Skills", "06-Adapters", "07-Kit"]
SKIP_NAMES = {".gitkeep", ".DS_Store"}

KNOWN_TEMPLATES = {"AGENTS.md", "SECURITY.md", "project-tracker.md",
                   "regression-cases.json", "runner.py", "install.sh", "README.md",
                   "settings.json", "harness.mdc", "copilot-instructions.md",
                   "pull_request_template.md", "harness.md"}

# 仅 A(母体) 侧出现且命中 → 预期分化（引用私有件/工作台特性，不该进 kit）
A_CUSTOM = [
    "05-Harness", "06-工具链/", "05-实战/", "01-调研/",
    "~/.workbuddy", "~/.codex", "~/.cursor", "~/.zcode",
    "pet_xiaoman", "张工", "宠宝树", "13+1",
    "MCP-工具分级", "工具治理白名单", "由 05-Harness", "skills-cursor",
    "四端", "四个副本", "跨工具", "WorkBuddy / Codex", "WorkBuddy 会话",
    "OPC 通用", "需手动同步", "06-Adapters/",
]

# 仅 B(分发) 侧出现且命中 → 预期分化（通用化/去隐私/本仓库自引用）
B_GENERIC = [
    "harness-kit", "contributors", "装机落位于本目录", "本仓库",
    "真实项目", "通用回归基线", "AGENTS.md 治理", "按你的团队",
    "· harness-kit", "当前版本同步", "版本管理与回滚约定",
    "runner_script_path", "report_path", "07-Kit/", "AI 工具",
    "生产级资产", "边界错位会写坏文件", "装机可选",
]

TREE_PREFIX = ("├── ", "└── ", "├─ ")
CHANGELOG_HINTS = ("git tag -a harness", "git checkout harness")
NEIGHBOR_WIN = 4
NOISE = {"", "```", "done", "---", "===", "~~~", "<!-- -->"}


def template_files(root):
    """扫描 root 下 4 个模板目录，返回相对路径集合。
    排除：模板目录的 .gitkeep/.DS_Store；运行时产物目录 reports/、__pycache__、
    .git（evals 基线报告是 05 实测私有输出，非模板，不参与比对）"""
    files = set()
    for sub in TEMPLATE_DIRS:
        base = os.path.join(root, sub)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, fnames in os.walk(base):
            dirnames[:] = [d for d in dirnames
                           if d not in ("reports", "__pycache__", ".git")]
            for fn in fnames:
                if fn in SKIP_NAMES:
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), root)
                files.add(rel)
    return files


def is_structure_noise(text):
    """结构噪音行：空行/代码围栏(含语言标注)/闭合符 —— 伴随归类只吞这类行，
    有实质内容的行即使紧邻命中行也保留待裁决（防真漂移被邻域误吞）"""
    t = text.strip()
    return t in NOISE or t.startswith("```") or t.startswith("~~~")


def hit_features(text, features):
    return [f for f in features if f in text]


def is_changelog(text):
    if text.lstrip().startswith("- "):
        return True
    return any(h in text for h in CHANGELOG_HINTS)


def is_tree_row(text):
    if not text.startswith(TREE_PREFIX):
        return False, ""
    m = re.search(r"[A-Za-z0-9_.-]+\.(?:md|json|py|sh)", text)
    if not m:
        return False, ""
    return m.group(0) in KNOWN_TEMPLATES, m.group(0)


def collect_events(fa, fb):
    out = subprocess.run(["diff", fa, fb], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    events = []
    for line in out.stdout.splitlines():
        if line.startswith("< "):
            events.append(("A", line[2:]))
        elif line.startswith("> "):
            events.append(("B", line[2:]))
    return events


def classify_pair(rel, a_dir, b_dir):
    fa, fb = os.path.join(a_dir, rel), os.path.join(b_dir, rel)
    events = collect_events(fa, fb)
    n = len(events)
    kind = ["pending"] * n          # custom | changelog | tree | neighbor | pending
    a_count = b_count = 0
    for i, (side, text) in enumerate(events):
        if side == "A":
            a_count += 1
        else:
            b_count += 1
        feats = A_CUSTOM if side == "A" else B_GENERIC
        if hit_features(text, feats):
            kind[i] = "custom"
    for i, (side, text) in enumerate(events):
        if kind[i] != "pending":
            continue
        if is_changelog(text):
            kind[i] = "changelog"
            continue
        ok, _ = is_tree_row(text)
        if ok:
            kind[i] = "tree"
    for i, (side, text) in enumerate(events):
        if kind[i] != "pending":
            continue
        if not is_structure_noise(text):
            continue  # 有实质内容不靠邻域归类，防误吞真漂移
        lo, hi = max(0, i - NEIGHBOR_WIN), min(n, i + NEIGHBOR_WIN + 1)
        if any(kind[j] in ("custom", "changelog", "tree") for j in range(lo, hi)):
            kind[i] = "neighbor"
    stats = {"a": a_count, "b": b_count,
             "custom": kind.count("custom"),
             "changelog": kind.count("changelog"),
             "tree": kind.count("tree"),
             "neighbor": kind.count("neighbor"),
             "pending": kind.count("pending")}
    pending = [(side, text) for k, (side, text) in zip(kind, events) if k == "pending"]
    return {"rel": rel, "stats": stats, "pending": pending}


def main():
    a_dir = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else A_DEFAULT
    b_dir = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else B_DEFAULT

    print(f"A(母体): {a_dir}")
    print(f"B(分发): {b_dir}")
    print(f"比对目录: {TEMPLATE_DIRS}\n")

    if not os.path.isdir(b_dir):
        print(f"❌ B 目录不存在: {b_dir}\n   先 git clone git@github.com:genapohub/harness-kit.git {b_dir}")
        sys.exit(1)

    # ---------- A. 文件级检查（结构性漂移） ----------
    a_files = template_files(a_dir)
    b_files = template_files(b_dir)
    only_a = sorted(a_files - b_files)
    only_b = sorted(b_files - a_files)
    structural = False
    if only_a:
        structural = True
        print("⚠️ 仅 A(母体) 有的模板文件 —— 疑似新增模板未同步进 kit:")
        for f in only_a:
            print(f"  - {f}")
    if only_b:
        structural = True
        print("⚠️ 仅 B(kit) 有的文件 —— kit 独有，确认是否有意:")
        for f in only_b:
            print(f"  - {f}")
    if structural:
        print("\n结论: 文件级漂移 → 先补齐/确认文件，再谈内容对齐")
        sys.exit(1)
    print("文件级: 两侧模板清单一致 ✅\n")

    # ---------- B. 内容级逐文件 diff ----------
    common = sorted(a_files & b_files)
    results = [classify_pair(rel, a_dir, b_dir) for rel in common]

    print("=" * 84)
    print(f"{'模板文件':<34}{'差异':>5}{'A独有':>6}{'B独有':>6}{'定制':>5}"
          f"{'历史':>5}{'目录树':>5}{'伴随':>5}{'待裁决':>6}")
    print("-" * 84)

    all_pending = []
    for r in results:
        s = r["stats"]
        print(f"{r['rel']:<34}{s['a'] + s['b']:>5}{s['a']:>6}{s['b']:>6}{s['custom']:>5}"
              f"{s['changelog']:>5}{s['tree']:>5}{s['neighbor']:>5}{s['pending']:>6}")
        all_pending.extend((r["rel"], side, t) for side, t in r["pending"])
    print("-" * 84)

    total_custom = sum(r["stats"]["custom"] for r in results)
    total_changelog = sum(r["stats"]["changelog"] for r in results)
    total_tree = sum(r["stats"]["tree"] for r in results)
    total_neighbor = sum(r["stats"]["neighbor"] for r in results)
    print(f"归类汇总: 预期分化 {total_custom} 行（母体定制/分发通用）｜ 版本历史 {total_changelog} 行"
          f"（各侧自维护，无需同步）｜ 目录树排版 {total_tree} 行 ｜ 伴随行 {total_neighbor} 行")
    print(f"待人工裁决: {len(all_pending)} 行\n")

    if all_pending:
        print("▼ 以下行未命中任何预期分化规则 —— 真漂移候选，请人工裁决:")
        cur = None
        for rel, side, text in all_pending:
            if rel != cur:
                print(f"\n  [{rel}]")
                cur = rel
            print(f"    {side}> {text}")
        print()

    print("=" * 84)
    if not all_pending:
        print("ALL CLEAR ✅ 差异全部为预期分化（母体定制 / 分发通用 / 版本历史 / 排版），无需同步")
    else:
        print(f"待裁决 {len(all_pending)} 行（见上）→ 人工裁决：属实增量则同步到另一侧；属等价改写则忽略")
    sys.exit(0)


if __name__ == "__main__":
    main()
