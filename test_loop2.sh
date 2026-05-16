#!/bin/bash
set -euo pipefail
REMOTE_PATH="gdrive:istohniki/Учебники сокращ для энологии"
VAULT_KNOWLEDGE="/tmp/test_knowledge"
TMP_DIR="/tmp/book_ingest_test"
LOG_FILE="/tmp/test.log"
mkdir -p "$VAULT_KNOWLEDGE" "$TMP_DIR"
log() { echo "[$(date +%Y-%m-%d %H:%M:%S)] $*" | tee -a "$LOG_FILE"; }
log "Start"
log "Found files via rclone ls:"
count=0
while IFS= read -r line || [[ -n $line ]]; do
  log "Inside loop: $line"
  line="${line#"${line%%[![:space:]]*}"}"
  log "After trim leading: $line"
  if [[ -z "$line" ]]; then
    log "Empty line, continue"
    continue
  fi
  size="${line%% *}"
  file="${line#* }"
  file="${file#"${file%%[![:space:]]*}"}"
  log "size=$size file=$file"
  if [[ -z "$file" ]]; then
    log "File empty, continue"
    continue
  fi
  ((count++))
  log "Processing: $size $file"
  filename=$(basename "$file")
  log "filename=$filename"
  note_basename="${filename%.*}"
  log "note_basename=$note_basename"
  note_file="$VAULT_KNOWLEDGE/${note_basename}.md"
  log "note_file=$note_file"
  if [[ -f "$note_file" ]]; then
    log "Note exists, skip"
    continue
  fi
  # break after 1
  if ((count >= 1)); then
    log "Breaking after 1"
    break
  fi
done < <(rclone ls "$REMOTE_PATH" 2>/dev/null)
log "Count: $count"
