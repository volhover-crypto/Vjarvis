#!/bin/bash
# Book Ingestion Script for Google Drive to Vault Knowledge Base
# Usage: ./ingest_books.sh <remote:path> [--max-chars N] [--dry-run]
# Example: ./ingest_books.sh gdrive:istohniki/"Учебники сокращ для энологии"

set -u

# Configuration
REMOTE_PATH="${1:-}"
if [[ -z "$REMOTE_PATH" ]]; then
  echo "Error: Remote path not provided."
  echo "Usage: $0 <remote:path> [--max-chars N] [--dry-run]"
  exit 1
fi

# Normalize remote path: remove trailing slash
REMOTE_PATH="${REMOTE_PATH%/}"

MAX_CHARS=2000
DRY_RUN=false

# Parse optional arguments
shift || true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --max-chars)
      MAX_CHARS="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Directories
VAULT_KNOWLEDGE="/root/vault/knowledge"
TMP_DIR="/tmp/book_ingest_$$"
LOG_FILE="/tmp/book_ingest_$$.log"

mkdir -p "$VAULT_KNOWLEDGE" "$TMP_DIR"
echo "Log file: $LOG_FILE" >&2

# Function to log messages
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

# Function to extract text based on extension
extract_text() {
  local src_file="$1"
  local dest_file="$2"
  local ext="${src_file##*.}"
  ext=$(echo "$ext" | tr '[:upper:]' '[:lower:]')
  
  case "$ext" in
    pdf)
      if command -v pdftotext >/dev/null 2>&1; then
        pdftotext "$src_file" "$dest_file"
      else
        log "ERROR: pdftotext not installed"
        return 1
      fi
      ;;
    djvu)
      if command -v djvutxt >/dev/null 2>&1; then
        djvutxt "$src_file" > "$dest_file"
      else
        log "WARNING: djvutxt not installed, skipping .djvu file"
        return 1
      fi
      ;;
    doc)
      if command -v antiword >/dev/null 2>&1; then
        antiword "$src_file" > "$dest_file"
      elif command -v pandoc >/dev/null 2>&1; then
        pandoc "$src_file" -t plain -o "$dest_file"
      else
        log "ERROR: Neither antiword nor pandoc installed for .doc"
        return 1
      fi
      ;;
    docx)
      if command -v pandoc >/dev/null 2>&1; then
        pandoc "$src_file" -t plain -o "$dest_file"
      else
        log "ERROR: pandoc not installed for .docx"
        return 1
      fi
      ;;
    fb2)
      if command -v fb2txt >/dev/null 2>&1; then
        fb2txt "$src_file" > "$dest_file"
      elif command -v pandoc >/dev/null 2>&1; then
        pandoc "$src_file" -t plain -o "$dest_file"
      else
        log "WARNING: No FB2 extractor found, skipping .fb2"
        return 1
      fi
      ;;
    md|txt)
      cp "$src_file" "$dest_file"
      ;;
    *)
      log "WARNING: Unsupported extension '.$ext', skipping"
      return 1
      ;;
  esac
}

# Function to create knowledge note from extracted text
create_note() {
  local src_file="$1"
  local extracted_file="$2"
  local note_file="$3"
  
  local filename=$(basename "$src_file")
  local basename="${filename%.*}"
  local title="$basename"
  
  # Get metadata via rclone stat (size, modification time)
  local mod_time size
  mod_time=$(rclone stat "$REMOTE_PATH/$filename" --no-mimetype --no-checksum 2>/dev/null | grep 'ModTime' | cut -d' ' -f3- || echo "unknown")
  size=$(rclone stat "$REMOTE_PATH/$filename" --no-mimetype --no-checksum 2>/dev/null | grep 'Size' | cut -d' ' -f2- || echo "unknown")
  
  # Extract first $MAX_CHARS characters for preview
  local preview
  if [[ -s "$extracted_file" ]]; then
    preview=$(cut -c -"$MAX_CHARS" "$extracted_file" | sed 's/$/\\n/' | head -c -1)
  else
    preview="(empty or extraction failed)"
  fi
  
  # Build note content
  cat > "$note_file" <<EOF
# $title

## Источник
- Файл: $filename
- Путь в Google Drive: $REMOTE_PATH/$filename
- Размер: $size байт
- Дата изменения: $mod_time
- Дата обработки: $(date '+%Y-%m-%d')

## Аннотация
Автоматически извлечённое превью (первые $MAX_CHARS символов):

\`\`\`
$preview
\`\`\`

## Ключевые темы
- Требует ручного заполнения после review

## Связанные знания
- Связь с другими заметками в vault/knowledge/ будет установлена через теги и ссылки после обработки.

## Статус обработки
- Извлечение текста: $( [[ -s "$extracted_file" ]] && echo "успешно" || echo "не удалось" )
- Размер извлечённого текста: $(wc -c < "$extracted_file") байт

## Дата обработки
$(date '+%Y-%m-%d %H:%M:%S')
EOF
}

# Main processing
log "Starting ingestion from $REMOTE_PATH"
log "Max chars per note: $MAX_CHARS"
log "Dry run: $DRY_RUN"

# List files (rclone ls outputs: size  filename)
log "Found files via rclone ls:"
count=0
while IFS= read -r line || [[ -n $line ]]; do
  # Remove leading spaces
  line="${line#"${line%%[![:space:]]*}"}"
  if [[ -z "$line" ]]; then
    continue
  fi
  # Split into size (first field) and filename (rest)
  size="${line%% *}"
  file="${line#* }"
  # Remove leading spaces from filename (in case there were multiple spaces)
  file="${file#"${file%%[![:space:]]*}"}"
  if [[ -z "$file" ]]; then
    continue
  fi
  ((count++))
  log "Processing: $size $file"
  
  # Extract filename without extension for note
  filename=$(basename "$file")
  note_basename="${filename%.*}"
  note_file="$VAULT_KNOWLEDGE/${note_basename}.md"
  if [[ -f "$note_file" ]]; then
    log "Note already exists, skipping: $note_file"
    continue
  fi
  
  # Copy file to temp
  src_tmp="$TMP_DIR/$filename"
  if [[ "$DRY_RUN" = false ]]; then
    log "Copying file to temporary location..."
    log "Source: $REMOTE_PATH/$file"
    rclone copy "$REMOTE_PATH/$file" "$TMP_DIR/" --progress 2>>"$LOG_FILE" || {
      log "ERROR: Failed to copy $filename"
      continue
    }
  else
    log "[DRY RUN] Would copy $REMOTE_PATH/$file to $TMP_DIR/"
  fi
  
  # Extract text
  extracted_file="$TMP_DIR/${note_basename}.extracted.txt"
  if [[ "$DRY_RUN" = false ]]; then
    log "Extracting text..."
    if extract_text "$src_tmp" "$extracted_file"; then
      log "Extraction successful"
    else
      log "Extraction failed or unsupported format"
      # Still create note with empty preview?
      : # continue to create note anyway
    fi
  else
    log "[DRY RUN] Would extract text from $src_tmp"
  fi
  
  # Create note
  if [[ "$DRY_RUN" = false ]]; then
    log "Creating knowledge note..."
    create_note "$src_tmp" "$extracted_file" "$note_file"
    log "Note created: $note_file"
    
    # Sync with GBrain
    log "Syncing vault with GBrain..."
    gbrain sync --repo /root/vault >>"$LOG_FILE" 2>&1 || log "GBrain sync warning"
    
    # Attempt embed (may fail)
    log "Attempting to embed stale chunks..."
    gbrain embed --stale >>"$LOG_FILE" 2>&1 || log "GBrain embed warning (expected if no model)"
    
    # Git add and commit
    log "Adding note to git..."
    cd /root/vault && git add "knowledge/$(basename "$note_file")" >>"$LOG_FILE" 2>&1
    git commit -m "Add knowledge note: $note_basename" >>"$LOG_FILE" 2>&1 || log "Git commit warning (maybe no changes)"
  else
    log "[DRY RUN] Would create note: $note_file"
    log "[DRY RUN] Would sync GBrain and embed"
    log "[DRY RUN] Would git add and commit"
  fi
  
  # Cleanup temp file for this iteration (keep temp dir for inspection if needed)
  if [[ "$DRY_RUN" = false ]]; then
    rm -f "$src_tmp" "$extracted_file"
  fi
done < <(rclone ls "$REMOTE_PATH" 2>/dev/null)

if [[ $count -eq 0 ]]; then
  log "No files found in $REMOTE_PATH"
  exit 0
fi
log "Found $count files"

# Final cleanup
if [[ "$DRY_RUN" = false ]]; then
  rm -rf "$TMP_DIR"
  log "Temporary directory cleaned up"
else
  log "[DRY RUN] Temporary directory left at: $TMP_DIR"
fi

log "Ingestion complete"