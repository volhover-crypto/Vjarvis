#!/bin/bash
set -euo pipefail
REMOTE_PATH="gdrive:istohniki/Учебники сокращ для энологии"
MAX_CHARS=2000
DRY_RUN=true
VAULT_KNOWLEDGE="/root/vault/knowledge"
TMP_DIR="/tmp/book_ingest_test"
LOG_FILE="/tmp/book_ingest_test.log"
mkdir -p "$VAULT_KNOWLEDGE" "$TMP_DIR"
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}
log "Found files via rclone ls:"
count=0
while IFS= read -r line || [[ -n $line ]]; do
  log "Inside loop: $line"
  ((count++))
  if ((count >= 2)); then
    break
  fi
done < <(rclone ls "$REMOTE_PATH" 2>/dev/null)
log "Count: $count"
