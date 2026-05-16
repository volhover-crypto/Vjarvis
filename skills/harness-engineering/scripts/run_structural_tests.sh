#!/usr/bin/env bash
# Placeholder for structural tests
echo "Running structural tests..."
# Example: check that all skills have SKILL.md and scripts/
failures=0
for skill_dir in /root/.openclaw/workspace/skills/*/; do
    if [[ -d "$skill_dir" && "$skill_dir" != */"scripts" && "$skill_dir" != */"references" ]]; then
        skill_name=$(basename "$skill_dir")
        if [[ ! -f "$skill_dir/SKILL.md" ]]; then
            echo "FAIL: $skill_name missing SKILL.md"
            ((failures++))
        fi
        if [[ ! -d "$skill_dir/scripts" ]]; then
            echo "WARN: $skill_name missing scripts/ directory"
        fi
    fi
done
if [[ $failures -eq 0 ]]; then
    echo "All structural checks passed."
    exit 0
else
    echo "Found $failures issue(s)."
    exit 1
fi