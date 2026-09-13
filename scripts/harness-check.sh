#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== Harness root check =="
for file in AGENTS.md project-tracker.md SECURITY.md .ai/SKILLS.md evals/runner.py evals/regression-cases.json; do
  if [ ! -f "$ROOT/$file" ]; then
    echo "missing: $file"
    exit 1
  fi
done

echo "== Skills check =="
SKILL_COUNT="$(find "$ROOT/skills" -mindepth 2 -maxdepth 2 -name SKILL.md -type f 2>/dev/null | wc -l | tr -d ' ')"
echo "skills: $SKILL_COUNT"
[ "$SKILL_COUNT" -gt 0 ] || { echo "no skills installed"; exit 1; }

echo "== Evals =="
python3 "$ROOT/evals/runner.py" "$ROOT" --since HEAD~1

echo "all checks passed"
