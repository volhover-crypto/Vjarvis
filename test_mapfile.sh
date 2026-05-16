#!/bin/bash
set -euo pipefail
REMOTE_PATH="gdrive:istohniki/Учебники сокращ для энологии"
log() { echo "$*"; }
log "Starting"
mapfile -t lines < <(rclone ls "$REMOTE_PATH" 2>/dev/null || true)
echo "Number of lines: ${#lines[@]}"
if [[ ${#lines[@]} -eq 0 ]]; then
  echo "No lines"
  exit 1
fi
count=0
for line in "${lines[@]}"; do
  echo "Processing line: $line"
  ((count++))
  if ((count >= 2)); then
    echo "Breaking after 2"
    break
  fi
done
echo "Count: $count"
