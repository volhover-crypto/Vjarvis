#!/bin/bash
set -euo pipefail
REMOTE_PATH="test"
log() { echo "[$(date +%H:%M:%S)] $*"; }
log "Starting"
log "Found files via rclone ls:"
count=0
while IFS= read -r line; do
  log "Inside loop: $line"
  ((count++))
done < <(echo -e "line1\nline2")
echo "Count: $count"
