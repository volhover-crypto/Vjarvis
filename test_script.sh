#!/bin/bash
set -euo pipefail
REMOTE_PATH="gdrive:istohniki/Учебники сокращ для энологии"
log() { echo "[$(date +%Y-%m-%d %H:%M:%S)] $*" | tee -a "$LOG_FILE"; }
LOG_FILE="/tmp/test.log"
mkdir -p "$(dirname "$LOG_FILE")"
echo "Log file: $LOG_FILE" >&2
log "Starting ingestion from $REMOTE_PATH"
log "Max chars per note: 2000"
log "Dry run: true"
log "Found files via rclone ls:"
count=0
while IFS= read -r line; do
  log "Inside loop: $line"
  ((count++))
done < <(rclone ls "$REMOTE_PATH" 2>/dev/null || true)
log "Count: $count"
