#!/bin/bash
set -u
REMOTE_PATH="gdrive:istohniki/Учебники сокращ для энологии"
count=0
while IFS= read -r line || [[ -n $line ]]; do
    echo "Line: $line"
    ((count++))
    if [[ $count -ge 2 ]]; then
        break
    fi
done < <(rclone ls "$REMOTE_PATH" 2>/dev/null)
echo "Count: $count"
