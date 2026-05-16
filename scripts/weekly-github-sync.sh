#!/bin/bash
# Weekly GitHub sync for Jarvis agent identity
# Runs every Sunday at 02:00 MSK

set -e

WORKSPACE="/root/.openclaw/workspace"
VAULT="/root/vault"
GIT_USER="Jarvis Agent"
GIT_EMAIL="jarvis1972@proton.me"

cd "$WORKSPACE"

# Configure git
git config user.name "$GIT_USER"
git config user.email "$GIT_EMAIL"

# Stage all changes
git add -A

# Commit if there are changes
if git diff --cached --quiet; then
    echo "No changes to commit"
else
    git commit -m "Weekly sync: $(date '+%Y-%m-%d %H:%M MSK')

Auto-sync of agent identity, memory, skills, and projects.
See MEMORY.md for latest state."
fi

# Push to GitHub remote (jarvis)
git push jarvis master 2>&1 || echo "Push failed — check auth"

echo "Weekly sync complete: $(date)"
