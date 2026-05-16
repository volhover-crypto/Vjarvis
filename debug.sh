#!/bin/bash
set -euo pipefail
REMOTE_PATH="gdrive:istohniki/Учебники сокращ для энологии"
log() { echo "[$(date +%H:%M:%S)] $*"; }
log "Starting"
log "Found files via rclone ls:"
count=0
while IFS= read -r line; do
    log "Read line: $line"
    # Remove leading spaces
    line="${line#"${line%%[![:space:]]*}"}"
    log "After trim: $line"
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
    # Simulate rest
    filename=$(basename "$file")
    note_basename="${filename%.*}"
    note_file="/tmp/test/$note_basename.md"
    log "note_file=$note_file"
    if [[ -f "$note_file" ]]; then
        log "Note exists, skip"
        continue
    fi
    # break after 2 for test
    if (( count >= 2 )); then
        log "Breaking after 2"
        break
    fi
done < <(rclone ls "$REMOTE_PATH" 2>/dev/null || true)
log "Total count: $count"
