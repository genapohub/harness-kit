#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE="${1:-/Users/macos/Downloads/WorkBuddy/日常办公/00-Skills汇总}"
TODAY="$(date +%Y-%m-%d)"

[ -d "$SOURCE" ] || { echo "技能源目录不存在: $SOURCE"; exit 1; }

mkdir -p "$ROOT/skills" "$ROOT/.ai"

copy_dir() {
  local src="$1"
  local dst="$2"
  mkdir -p "$dst"
  command -v rsync >/dev/null 2>&1 || { echo "缺少 rsync，无法安全刷新 skills"; exit 1; }
  rsync -a --delete --exclude '.git' --exclude '__pycache__' --exclude '.DS_Store' "$src"/ "$dst"/
}

installed=()
while IFS= read -r skill_file; do
  skill_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$skill_dir")"
  copy_dir "$skill_dir" "$ROOT/skills/$skill_name"
  installed+=("$skill_name")
done < <(find "$SOURCE" -mindepth 2 -maxdepth 3 -name SKILL.md -type f | sort)

{
  echo "# 项目已安装 Skills"
  echo ""
  echo "来源: $SOURCE"
  echo "同步日期: $TODAY"
  echo ""
  echo "| Skill | 路径 |"
  echo "|---|---|"
  for name in "${installed[@]}"; do
    echo "| $name | skills/$name |"
  done
} > "$ROOT/.ai/SKILLS.md"

echo "skills refreshed: ${#installed[@]}"
