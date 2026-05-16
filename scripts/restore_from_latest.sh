#!/usr/bin/env bash
set -euo pipefail

# Configuration
BACKUP_BASE="/root/.openclaw/workspace/backup"
WORKSPACE="/root/.openclaw/workspace"
MEMORY_FILE="${WORKSPACE}/MEMORY.md"
SKILLS_DIR="${WORKSPACE}/skills"
LOG_FILE="/root/.openclaw/workspace/logs/restore_latest_$(date +%Y%m%d_%H%M%S).log"

# Ensure log directory exists
mkdir -p "$(dirname "${LOG_FILE}")"

# Logging function
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" | tee -a "${LOG_FILE}"
}

log "=== Starting restore from latest point ==="

# Find latest backup directory
if [[ ! -d "${BACKUP_BASE}" ]]; then
    log "ERROR: Backup base directory not found: ${BACKUP_BASE}"
    exit 1
fi

LATEST_BACKUP=$(ls -1td "${BACKUP_BASE}"/restore_* 2>/dev/null | head -1 || echo "")

if [[ -z "${LATEST_BACKUP}" ]]; then
    log "ERROR: No backup directories found in ${BACKUP_BASE}"
    exit 1
fi

log "Latest backup found: ${LATEST_BACKUP}"

# Check if MEMORY.md exists in backup
BACKUP_MEMORY="${LATEST_BACKUP}/MEMORY.md"
if [[ ! -f "${BACKUP_MEMORY}" ]]; then
    log "WARNING: MEMORY.md not found in backup. Skipping memory restore."
else
    log "Restoring MEMORY.md from backup..."
    # Backup current memory if exists
    if [[ -f "${MEMORY_FILE}" ]]; then
        cp "${MEMORY_FILE}" "${MEMORY_FILE}.bak.$(date +%Y%m%d_%H%M%S)"
        log "Current MEMORY.md backed up."
    fi
    cp "${BACKUP_MEMORY}" "${MEMORY_FILE}"
    log "MEMORY.md restored from backup."
fi

# Restore skills directory if backup exists
BACKUP_SKILLS_DIR="${LATEST_BACKUP}/skills_backup"
if [[ -d "${BACKUP_SKILLS_DIR}" ]]; then
    log "Restoring skills directory from backup..."
    # Backup current skills if exists
    if [[ -d "${SKILLS_DIR}" ]]; then
        mv "${SKILLS_DIR}" "${SKILLS_DIR}.bak.$(date +%Y%m%d_%H%M%S)"
        log "Current skills directory backed up."
    fi
    cp -r "${BACKUP_SKILLS_DIR}" "${SKILLS_DIR}"
    log "Skills directory restored from backup."
else
    # Fallback to just skills list if no full backup
    BACKUP_SKILLS_LIST="${LATEST_BACKUP}/skills.txt"
    if [[ -f "${BACKUP_SKILLS_LIST}" ]]; then
        log "Skills list available in backup: ${BACKUP_SKILLS_LIST}"
        log "To restore skills, manually copy from backup or use Git recovery."
    else
        log "No skills list or backup found in backup."
    fi
fi

# Show summary
log "=== Restore process completed ==="
log "Latest backup: ${LATEST_BACKUP}"
log "Memory restored: ${MEMORY_FILE} (if backup existed)"
log "Skills: restored from backup if available, otherwise refer to backup skills.txt for list."
log "For full recovery, follow instructions in MEMORY.md section '🚨 Восстановление после сбоя'."

exit 0