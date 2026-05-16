#!/bin/bash
set -euo pipefail
REMOTE_PATH="gdrive:istohniki/Учебники сокращ для энологии"
log() { echo "[$(date +%H:%M:%S)] $*"; }
log "Start"
log "Found files via rclone ls:"
count=0
while IFS= read -r line || [[ -n $line ]]; do
  log "Inside: $line"
  ((count++))
  if ((count >= 2)); then
    log "Breaking"
    break
  fi
done < <(rclone ls "$REMOTE_PATH" 2>/dev/null)
log "Count: $count"
