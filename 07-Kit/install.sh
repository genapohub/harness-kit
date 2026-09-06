#!/usr/bin/env bash
# install.sh · Harness 一条命令装机
# 用法: bash install.sh /path/to/项目
#
# 做什么:
#   1. 把 AGENTS.md / project-tracker.md / SECURITY.md 落位到项目根目录
#   2. 自动填项目名、预填 P0 激活角色、修复模板里指向工作区的路径断链
#   3. 检测嵌套独立 git 仓库并从根仓库隔离（.gitignore）
#   4. git init + 初始 commit + harness tag（Day1 版本控制）
# 模板来源: 本仓库 02-规范、03-状态 原件（单一事实源，本脚本不持有拷贝）

set -euo pipefail

HARNESS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"   # harness-kit 仓库根目录
HARNESS_VERSION="v1.4"                             # 与 AGENTS.md 当前版本同步
TODAY="$(date +%Y-%m-%d)"
OWNER="$(git config user.name 2>/dev/null || echo "${USER:-owner}")"   # 责任人: 取本机 git 配置（分发友好，不写死）

TARGET_RAW="${1:?用法: bash install.sh /path/to/项目}"
[ -d "$TARGET_RAW" ] || { echo "❌ 目录不存在: $TARGET_RAW"; exit 1; }
TARGET="$(cd "$TARGET_RAW" && pwd)"
NAME="$(basename "$TARGET")"

[ -f "$TARGET/AGENTS.md" ] && { echo "❌ $TARGET 已有 AGENTS.md，中止（防覆盖）"; exit 1; }
[ -f "$HARNESS_ROOT/02-规范/AGENTS.md" ] || { echo "❌ 找不到模板: $HARNESS_ROOT/02-规范/AGENTS.md"; exit 1; }
[ -f "$HARNESS_ROOT/03-状态/project-tracker.md" ] || { echo "❌ 找不到模板: $HARNESS_ROOT/03-状态/project-tracker.md"; exit 1; }
[ -f "$HARNESS_ROOT/02-规范/SECURITY.md" ] || { echo "❌ 找不到模板: $HARNESS_ROOT/02-规范/SECURITY.md"; exit 1; }

echo "▶ 装机目标: $TARGET"

# ---------- 1. AGENTS.md（宪法）----------
# 顺序敏感: 专项引用先落到中间 token，通用目录前缀替换跑完后再还原为绝对路径，
#           避免替换产物（含 06-工具链/ 等前缀）再次命中通用规则造成双重前缀
sed \
  -e "s|项目名：【你的项目名】|项目名：$NAME|" \
  -e "s|代码仓库：git@github.com:org/repo.git|代码仓库：本地仓库（远程待配）|" \
  -e "s|P0_常驻：【.*，按项目类型删减】|P0_常驻：tech-lead-guide / frontend-dev-guide / backend-dev-guide / qa-testing-guide / devops-guide / team-orchestrator|" \
  -e "s|03-状态/project-tracker.md = 任务状态持久化|project-tracker.md = 任务状态持久化（本目录）|" \
  -e "s|04-Evals/|$HARNESS_ROOT/04-Evals/|g" \
  -e "s|06-工具链/|$HARNESS_ROOT/06-工具链/|g" \
  -e "s|07-Kit/install.sh = |$HARNESS_ROOT/07-Kit/install.sh = |" \
  "$HARNESS_ROOT/02-规范/AGENTS.md" > "$TARGET/AGENTS.md"

# ---------- 2. project-tracker.md（状态单一事实源）----------
sed \
  -e "s|项目名：【项目名】|项目名：$NAME|" \
  -e "s|责任人：【你的名字】|责任人：$OWNER|" \
  -e "s|创建日期：【YYYY-MM-DD】|创建日期：$TODAY|" \
  -e "s|最后更新：【YYYY-MM-DD】|最后更新：$TODAY|" \
  -e "s|关联 AGENTS.md：【AGENTS.md 路径】|关联 AGENTS.md：AGENTS.md（本目录）|" \
  -e "s|关联仓库：【git@github.com:org/repo.git】|关联仓库：本地仓库（远程待配）|" \
  -e "s|当前分支：【branch】|当前分支：main|" \
  -e "s|Harness 版本：v1.0|Harness 版本：$HARNESS_VERSION|" \
  "$HARNESS_ROOT/03-状态/project-tracker.md" > "$TARGET/project-tracker.md"

# ---------- 3. SECURITY.md（通用规范，无项目占位符，直接复制）----------
cp "$HARNESS_ROOT/02-规范/SECURITY.md" "$TARGET/SECURITY.md"

# ---------- 4. 嵌套 git 仓库隔离（必须在根 git init 之前检测）----------
cd "$TARGET"
touch .gitignore
grep -qx '.DS_Store' .gitignore || echo '.DS_Store' >> .gitignore
grep -qx '.workbuddy/' .gitignore || echo '.workbuddy/' >> .gitignore   # AI 工具的会话记忆目录不入项目仓库

# 找子目录里的独立 git 仓库（mindepth 2 排除根自身，maxdepth 3 防误扫过深）
find . -mindepth 2 -maxdepth 3 -name .git -type d 2>/dev/null | while IFS= read -r gitdir; do
  rel="$(dirname "$gitdir")"
  rel="${rel#./}"
  if grep -qxF "${rel}" .gitignore; then
    echo "ℹ️  嵌套仓库已在 ignore 列表: ${rel}"
  else
    echo "${rel}" >> .gitignore
    echo "⚠️  嵌套独立 git 仓库已从根仓库隔离: ${rel}（代码仓库继续独立管理）"
  fi
done

# ---------- 5. Day1 版本控制: git init + commit + harness tag ----------
git init -b main >/dev/null 2>&1 || { git init >/dev/null 2>&1; git symbolic-ref HEAD refs/heads/main; }
git add -A
git commit -q -m "chore: harness 装机（AGENTS.md $HARNESS_VERSION + project-tracker v1.0 + SECURITY.md v1.0）"
if ! git tag -l | grep -qx "harness-$HARNESS_VERSION"; then
  git tag -a "harness-$HARNESS_VERSION" -m "Harness 基线：装机模板 $HARNESS_VERSION"
fi

# ---------- 6. 完成报告 ----------
LEFT=$(grep -c '【' "$TARGET/AGENTS.md" "$TARGET/project-tracker.md" 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
echo ""
echo "✅ 装机完成: $TARGET"
echo "   根仓库: $(git log --oneline -1 | head -c 60)…  tag: harness-$HARNESS_VERSION"
echo "   剩余占位符: $LEFT 处"
echo ""
echo "手工待办（约 5 分钟）:"
echo "  1. AGENTS.md 第一部分: 项目目标 / 目标用户 / 技术栈 / 当前阶段 + 项目知识地图"
echo "  2. AGENTS.md 第二部分: P1_阶段激活 按需勾选（product-plan / ux-design / data-analyst）"
echo "  3. project-tracker.md: 「当前阶段总览」写一句话 + 清掉已完成任务/决策日志里的模板示例行"
