#!/usr/bin/env bash
set -euo pipefail

# Configuration
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR="/root/.openclaw/workspace/backup/restore_${TIMESTAMP}"
MEMORY_FILE="/root/.openclaw/workspace/MEMORY.md"
RCLONE_CONFIG="/root/.openclaw/secrets/rclone.conf"
GDRIVE_REMOTE="gdrive"
GDRIVE_PATH="OpenClaw/RestorePoints/restore_${TIMESTAMP}"
LOG_FILE="/root/.openclaw/workspace/logs/restore_point_${TIMESTAMP}.log"

# Ensure directories exist
mkdir -p "${BACKUP_DIR}"
mkdir -p "$(dirname "${LOG_FILE}")"

# Logging function
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a "${LOG_FILE}"
}

log "Starting restore point creation: ${TIMESTAMP}"

# 1. System status
log "Collecting system status..."
openclaw gateway status > "${BACKUP_DIR}/system_status.txt" 2>&1 || true

# 2. Skills list and backup
log "Listing skills..."
ls -1 /root/.openclaw/workspace/skills/ > "${BACKUP_DIR}/skills.txt" 2>&1 || true
log "Backing up skills directory..."
cp -r /root/.openclaw/workspace/skills "${BACKUP_DIR}/skills_backup" 2>&1 || true

# 3. Tools documentation
log "Copying tools documentation..."
cp /root/.openclaw/workspace/TOOLS.md "${BACKUP_DIR}/TOOLS.md" 2>&1 || true

# 4. Accesses and tokens (relevant sections from MEMORY.md)
log "Extracting accesses from MEMORY.md..."
grep -A 20 "🔐 Доступы и токены" "${MEMORY_FILE}" > "${BACKUP_DIR}/accesses.txt" 2>&1 || true
# Also copy the whole MEMORY.md for completeness
cp "${MEMORY_FILE}" "${BACKUP_DIR}/MEMORY.md" 2>&1 || true

# 5. Resource usage
log "Collecting resource usage..."
{
    echo "=== Disk Usage ==="
    df -h
    echo -e "\n=== Memory Usage ==="
    free -h
    echo -e "\n=== Uptime ==="
    uptime
} > "${BACKUP_DIR}/resources.txt" 2>&1 || true

# 6. Create summary markdown
log "Creating summary..."
cat > "${BACKUP_DIR}/SUMMARY.md" <<EOF
# Restore Point Summary
**Timestamp:** ${TIMESTAMP}
**Host:** $(hostname)
**OpenClaw Version:** $(openclaw gateway status 2>/dev/null | head -1 || echo "unknown")

## Contents
- system_status.txt
- skills.txt
- skills_backup/ (full skills directory)
- TOOLS.md
- accesses.txt (excerpt from MEMORY.md)
- MEMORY.md (full copy)
- resources.txt

## How to restore
1. Download this directory from Google Drive remote '${GDRIVE_REMOTE}:${GDRIVE_PATH}' (if upload succeeded) or from local backup at ${BACKUP_DIR}
2. Copy relevant files back to their locations:
   - MEMORY.md -> /root/.openclaw/workspace/MEMORY.md
   - SKILLS: restore skills directory if needed
   - etc.
EOF

# 7. Append note to MEMORY.md (long-term memory)
log "Appending note to MEMORY.md..."
{
    echo ""
    echo "## [${TIMESTAMP}] Точка восстановления создана"
    echo "- Описание: ${BACKUP_DIR}/SUMMARY.md"
    echo "- Навыки: перечислены в skills.txt, полная копия в skills_backup/"
    echo "- Доступы: извлечены из MEMORY.md"
    echo "- Ресурсы: resources.txt"
    echo "- Локальная копия: ${BACKUP_DIR}"
} >> "${MEMORY_FILE}"

# 8. Attempt upload to Google Drive (may fail due to scopes)
log "Attempting upload to Google Drive..."
if rclone copy "${BACKUP_DIR}" "${GDRIVE_REMOTE}:${GDRIVE_PATH}" --config "${RCLONE_CONFIG}" --log-level INFO >> "${LOG_FILE}" 2>&1; then
    log "Upload successful to Google Drive: ${GDRIVE_REMOTE}:${GDRIVE_PATH}"
    echo ""
    echo "- Загружено в Google Drive: ${GDRIVE_REMOTE}:${GDRIVE_PATH}" >> "${MEMORY_FILE}"
else
    log "WARNING: Upload to Google Drive failed (likely insufficient scopes). Backup stored locally only."
    echo ""
    echo "- Загрузка в Google Drive НЕ УДАЛАСЬ (недостаточно прав scopes). Резервная копия хранится только локально." >> "${MEMORY_FILE}"
fi

log "Restore point creation completed."
log "Backup location: ${BACKUP_DIR}"
exit 0