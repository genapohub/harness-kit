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
HARNESS_VERSION="v1.5"                             # 与 AGENTS.md 当前版本同步
TODAY="$(date +%Y-%m-%d)"
OWNER="$(git config user.name 2>/dev/null || echo "${USER:-owner}")"   # 责任人: 取本机 git 配置（分发友好，不写死）
WITH_LOCAL_SKILLS=0
WITH_ADAPTERS=0
DEFAULT_SKILLS_SOURCE="$HARNESS_ROOT/../../00-Skills汇总"
SKILLS_SOURCE="$DEFAULT_SKILLS_SOURCE"
SKILLS_SOURCE_RESOLVED=""

usage() {
  cat <<'EOF'
用法:
  bash install.sh /path/to/项目 [--with-local-skills] [--skills-source /path/to/00-Skills汇总] [--with-adapters]

参数:
  --with-local-skills        把本地 00-Skills汇总 中包含 SKILL.md 的角色技能安装到目标项目 skills/
  --skills-source PATH       指定本地技能源目录，需配合 --with-local-skills 使用
  --with-adapters            安装 Claude / Cursor / GitHub Copilot / Kiro 适配文件
EOF
}

[ $# -ge 1 ] || { usage; exit 1; }
TARGET_RAW="$1"
shift || true

while [ $# -gt 0 ]; do
  case "$1" in
    --with-local-skills)
      WITH_LOCAL_SKILLS=1
      shift
      ;;
    --skills-source)
      [ $# -ge 2 ] || { echo "❌ --skills-source 缺少路径"; exit 1; }
      SKILLS_SOURCE="$2"
      shift 2
      ;;
    --with-adapters)
      WITH_ADAPTERS=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "❌ 未知参数: $1"
      usage
      exit 1
      ;;
  esac
done

[ -d "$TARGET_RAW" ] || { echo "❌ 目录不存在: $TARGET_RAW"; exit 1; }
TARGET="$(cd "$TARGET_RAW" && pwd)"
NAME="$(basename "$TARGET")"

[ -f "$TARGET/AGENTS.md" ] && { echo "❌ $TARGET 已有 AGENTS.md，中止（防覆盖）"; exit 1; }
[ -f "$HARNESS_ROOT/02-规范/AGENTS.md" ] || { echo "❌ 找不到模板: $HARNESS_ROOT/02-规范/AGENTS.md"; exit 1; }
[ -f "$HARNESS_ROOT/03-状态/project-tracker.md" ] || { echo "❌ 找不到模板: $HARNESS_ROOT/03-状态/project-tracker.md"; exit 1; }
[ -f "$HARNESS_ROOT/02-规范/SECURITY.md" ] || { echo "❌ 找不到模板: $HARNESS_ROOT/02-规范/SECURITY.md"; exit 1; }
[ "$WITH_LOCAL_SKILLS" -eq 0 ] || [ -d "$SKILLS_SOURCE" ] || { echo "❌ 技能源目录不存在: $SKILLS_SOURCE"; exit 1; }
[ "$WITH_ADAPTERS" -eq 0 ] || [ -d "$HARNESS_ROOT/06-Adapters" ] || { echo "❌ 找不到适配模板: $HARNESS_ROOT/06-Adapters"; exit 1; }
[ "$WITH_LOCAL_SKILLS" -eq 0 ] || SKILLS_SOURCE_RESOLVED="$(cd "$SKILLS_SOURCE" && pwd)"

echo "▶ 装机目标: $TARGET"

copy_dir() {
  local src="$1"
  local dst="$2"
  [ -d "$src" ] || return 0
  mkdir -p "$dst"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --exclude '.git' --exclude '__pycache__' --exclude '.DS_Store' "$src"/ "$dst"/
  else
    (cd "$src" && tar --exclude='.git' --exclude='__pycache__' --exclude='.DS_Store' -cf - .) | (cd "$dst" && tar -xf -)
  fi
}

install_local_skills() {
  local source_dir="$1"
  local installed=0
  mkdir -p "$TARGET/skills" "$TARGET/.ai"
  : > "$TARGET/.ai/SKILLS.md.tmp"
  {
    echo "# 项目已安装 Skills"
    echo ""
    echo "来源: $source_dir"
    echo "安装日期: $TODAY"
    echo ""
    echo "| Skill | 路径 | 状态 |"
    echo "|---|---|---|"
  } >> "$TARGET/.ai/SKILLS.md.tmp"

  while IFS= read -r skill_file; do
    skill_dir="$(dirname "$skill_file")"
    skill_name="$(basename "$skill_dir")"
    dst="$TARGET/skills/$skill_name"
    if [ -e "$dst" ]; then
      echo "| $skill_name | skills/$skill_name | 已存在，跳过 |" >> "$TARGET/.ai/SKILLS.md.tmp"
      continue
    fi
    copy_dir "$skill_dir" "$dst"
    installed=$((installed + 1))
    echo "| $skill_name | skills/$skill_name | 已安装 |" >> "$TARGET/.ai/SKILLS.md.tmp"
  done < <(find "$source_dir" -mindepth 2 -maxdepth 3 -name SKILL.md -type f | sort)

  mv "$TARGET/.ai/SKILLS.md.tmp" "$TARGET/.ai/SKILLS.md"
  echo "✅ 本地 Skills 接入完成: $installed 个新技能"
}

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

# ---------- 4. 可选: 本地 Skills / 多工具适配 ----------
if [ "$WITH_LOCAL_SKILLS" -eq 1 ]; then
  install_local_skills "$SKILLS_SOURCE_RESOLVED"
fi

if [ "$WITH_ADAPTERS" -eq 1 ]; then
  copy_dir "$HARNESS_ROOT/06-Adapters" "$TARGET"
  echo "✅ 多工具适配文件已安装"
fi

# ---------- 5. 嵌套 git 仓库隔离（必须在根 git init 之前检测）----------
cd "$TARGET"
touch .gitignore
grep -qx '.DS_Store' .gitignore || echo '.DS_Store' >> .gitignore
grep -qx '.workbuddy/' .gitignore || echo '.workbuddy/' >> .gitignore   # AI 工具的会话记忆目录不入项目仓库
grep -qx 'skills/*/.git/' .gitignore || echo 'skills/*/.git/' >> .gitignore

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

# ---------- 6. Day1 版本控制: git init + commit + harness tag ----------
git init -b main >/dev/null 2>&1 || { git init >/dev/null 2>&1; git symbolic-ref HEAD refs/heads/main; }
git add -A
git commit -q -m "chore: install harness governance ($HARNESS_VERSION)"
if ! git tag -l | grep -qx "harness-$HARNESS_VERSION"; then
  git tag -a "harness-$HARNESS_VERSION" -m "Harness 基线：装机模板 $HARNESS_VERSION"
fi

# ---------- 7. 完成报告 ----------
LEFT=$(grep -c '【' "$TARGET/AGENTS.md" "$TARGET/project-tracker.md" 2>/dev/null | awk -F: '{s+=$2} END {print s+0}')
echo ""
echo "✅ 装机完成: $TARGET"
echo "   根仓库: $(git log --oneline -1 | head -c 60)…  tag: harness-$HARNESS_VERSION"
echo "   剩余占位符: $LEFT 处"
[ "$WITH_LOCAL_SKILLS" -eq 1 ] && echo "   Skills: 已接入 $SKILLS_SOURCE_RESOLVED"
[ "$WITH_ADAPTERS" -eq 1 ] && echo "   Adapters: 已接入 Claude / Cursor / GitHub Copilot / Kiro"
echo ""
echo "手工待办（约 5 分钟）:"
echo "  1. AGENTS.md 第一部分: 项目目标 / 目标用户 / 技术栈 / 当前阶段 + 项目知识地图"
echo "  2. AGENTS.md 第二部分: P1_阶段激活 按需勾选（product-plan / ui-designer / data-analyst）"
echo "  3. project-tracker.md: 「当前阶段总览」写一句话 + 清掉已完成任务/决策日志里的模板示例行"
