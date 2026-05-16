#!/bin/bash
# Book Ingestion Script for Google Drive to Vault Knowledge Base
# Usage: ./ingest_books.sh <remote:path> [--max-chars N] [--dry-run]
# Example: ./ingest_books.sh gdrive:istohniki/"Учебники сокращ для энологии"

# NOTE: We do NOT use set -e across the whole script, because the loop
# body is allowed to fail on individual files without aborting the batch.
set -uo pipefail

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

# Supported extensions (lowercase)
SUPPORTED_EXT="pdf|djvu|doc|docx|fb2|md|txt"

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
  ext="${ext,,}"  # lowercase (bash 4+)
  
  case "$ext" in
    pdf)
      if command -v pdftotext >/dev/null 2>&1; then
        pdftotext "$src_file" "$dest_file" 2>/dev/null
        # Check if pdftotext produced meaningful text (>50 bytes)
        if [[ -f "$dest_file" ]] && [[ $(wc -c < "$dest_file") -lt 50 ]]; then
          log "  -> pdftotext produced empty/short output, trying OCR..."
          ocr_extract "$src_file" "$dest_file" "pdf"
        fi
      else
        log "ERROR: pdftotext not installed"
        return 1
      fi
      ;;
    djvu)
      if command -v djvutxt >/dev/null 2>&1; then
        djvutxt "$src_file" > "$dest_file" 2>/dev/null
        # Check if djvutxt produced meaningful text
        if [[ -f "$dest_file" ]] && [[ $(wc -c < "$dest_file") -lt 50 ]]; then
          log "  -> djvutxt produced empty/short output, trying OCR..."
          ocr_extract "$src_file" "$dest_file" "djvu"
        fi
      else
        log "WARNING: djvutxt not installed, skipping .djvu"
        return 1
      fi
      ;;
    doc)
      if command -v antiword >/dev/null 2>&1; then
        antiword "$src_file" > "$dest_file" 2>/dev/null
      elif command -v pandoc >/dev/null 2>&1; then
        pandoc "$src_file" -t plain -o "$dest_file" 2>/dev/null
      else
        log "ERROR: Neither antiword nor pandoc installed for .doc"
        return 1
      fi
      ;;
    docx)
      if command -v pandoc >/dev/null 2>&1; then
        pandoc "$src_file" -t plain -o "$dest_file" 2>/dev/null
      else
        log "ERROR: pandoc not installed for .docx"
        return 1
      fi
      ;;
    fb2)
      if command -v fb2txt >/dev/null 2>&1; then
        fb2txt "$src_file" > "$dest_file" 2>/dev/null
      elif command -v pandoc >/dev/null 2>&1; then
        pandoc "$src_file" -t plain -o "$dest_file" 2>/dev/null
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

# Function to extract text via OCR (tesseract)
ocr_extract() {
  local src_file="$1"
  local dest_file="$2"
  local src_type="$3"
  
  if ! command -v tesseract >/dev/null 2>&1; then
    log "  -> WARNING: tesseract not installed, skipping OCR"
    return 1
  fi
  
  local tmp_dir
  tmp_dir=$(mktemp -d)
  
  if [[ "$src_type" == "pdf" ]]; then
    # Convert PDF pages to images using pdftoppm
    if command -v pdftoppm >/dev/null 2>&1; then
      pdftoppm -png -r 300 "$src_file" "$tmp_dir/page" 2>/dev/null
      local pages=()
      for f in "$tmp_dir"/page-*.png; do
        [[ -f "$f" ]] && pages+=("$f")
      done
      if [[ ${#pages[@]} -eq 0 ]]; then
        log "  -> WARNING: pdftoppm produced no images"
        rm -rf "$tmp_dir"
        return 1
      fi
      log "  -> OCR: processing ${#pages[@]} pages with tesseract..."
      # Limit OCR to first 50 pages to avoid OOM
      local ocr_limit=50
      if [[ ${#pages[@]} -gt $ocr_limit ]]; then
        log "  -> OCR: limiting to first $ocr_limit of ${#pages[@]} pages"
        pages=("${pages[@]:0:$ocr_limit}")
      fi
      > "$dest_file"
      for page in "${pages[@]}"; do
        tesseract "$page" - -l rus+eng 2>/dev/null >> "$dest_file"
      done
    else
      log "  -> WARNING: pdftoppm not installed, cannot OCR PDF"
      rm -rf "$tmp_dir"
      return 1
    fi
  elif [[ "$src_type" == "djvu" ]]; then
    # Convert DJVU to images using ddjvu, page by page
    if command -v ddjvu >/dev/null 2>&1; then
      # Get number of pages
      local page_count
      page_count=$(ddjvu -format=tiff "$src_file" /dev/null 2>&1 | grep -oP '\d+(?= pages)' || echo "0")
      [[ -z "$page_count" || "$page_count" == "0" ]] && page_count=1
      # Limit OCR to first 50 pages to avoid OOM
      local ocr_limit=50
      if [[ $page_count -gt $ocr_limit ]]; then
        log "  -> OCR: limiting to first $ocr_limit of $page_count pages"
        page_count=$ocr_limit
      fi
      log "  -> OCR: processing $page_count DJVU pages with tesseract..."
      > "$dest_file"
      for ((i=1; i<=page_count; i++)); do
        local page_tif="$tmp_dir/page_$(printf '%04d' $i).tiff"
        ddjvu -format=tiff -page=$i "$src_file" "$page_tif" 2>/dev/null
        if [[ -f "$page_tif" ]]; then
          tesseract "$page_tif" - -l rus+eng 2>/dev/null >> "$dest_file"
          rm -f "$page_tif"
        fi
      done
    else
      log "  -> WARNING: ddjvu not installed, cannot OCR DJVU"
      rm -rf "$tmp_dir"
      return 1
    fi
  fi
  
  rm -rf "$tmp_dir"
  
  if [[ -f "$dest_file" ]] && [[ $(wc -c < "$dest_file") -gt 50 ]]; then
    log "  -> OCR: extracted $(wc -c < "$dest_file") bytes"
    return 0
  else
    log "  -> WARNING: OCR produced no meaningful text"
    return 1
  fi
}

# Function to create knowledge note from extracted text
create_note() {
  local src_file="$1"
  local extracted_file="$2"
  local note_file="$3"
  
  local filename
  filename=$(basename "$src_file")
  local basename="${filename%.*}"
  local title="$basename"
  
  # Get metadata via rclone stat (size, modification time)
  local mod_time="unknown"
  local size="unknown"
  if [[ "$DRY_RUN" = false ]]; then
    mod_time=$(rclone stat "$REMOTE_PATH/$filename" --no-mimetype --no-checksum 2>/dev/null \
      | grep 'ModTime' | cut -d' ' -f3- || true)
    size=$(rclone stat "$REMOTE_PATH/$filename" --no-mimetype --no-checksum 2>/dev/null \
      | grep 'Size' | cut -d' ' -f2- || true)
    [[ -z "$mod_time" ]] && mod_time="unknown"
    [[ -z "$size" ]] && size="unknown"
  fi
  
  # Extract first $MAX_CHARS characters for preview
  local preview
  if [[ -s "$extracted_file" ]]; then
    preview=$(cut -c -"$MAX_CHARS" "$extracted_file" | head -c 500)
    if [[ "$(wc -c < "$extracted_file")" -gt 500 ]]; then
      preview="${preview}..."
    fi
  else
    preview="(empty or extraction failed)"
  fi
  
  # Determine extraction status
  local extract_status="не удалось"
  [[ -s "$extracted_file" ]] && extract_status="успешно"
  local extracted_size=0
  [[ -f "$extracted_file" ]] && extracted_size=$(wc -c < "$extracted_file")
  
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
- Извлечение текста: $extract_status
- Размер извлечённого текста: $extracted_size байт

## Дата обработки
$(date '+%Y-%m-%d %H:%M:%S')
EOF
}

# Main processing
log "=========================================="
log "Starting ingestion from $REMOTE_PATH"
log "Max chars per note: $MAX_CHARS"
log "Dry run: $DRY_RUN"
log "=========================================="

# Read file list into array first — rclone ls outputs: "  SIZE  FILENAME"
# Filter to supported extensions only, skip subdirectories with / in name
mapfile -t all_lines < <(rclone lsl "$REMOTE_PATH" --max-depth 1 2>/dev/null | grep -v '^;' || true)

count=0
skipped=0
errors=0

for line in "${all_lines[@]}"; do
  # Skip empty lines
  [[ -z "$line" ]] && continue
  
  # Parse rclone lsl output: "SIZE  MODTIME  FILENAME"
  # rclone lsl format: "  1234567  2024-01-01 00:00:00.000000000  filename"
  # Use awk for reliable parsing
  size=$(echo "$line" | awk '{print $1}')
  filename=$(echo "$line" | awk '{$1=""; $2=""; $3=""; print $0}' | sed 's/^ *//')
  
  # Skip if no filename
  [[ -z "$filename" ]] && continue
  
  # Skip subdirectories
  [[ "$filename" == */ ]] && continue
  
  # Skip files in subdirectories (contain /)
  [[ "$filename" == *"/"* ]] && continue
  
  # Check extension
  ext="${filename##*.}"
  ext="${ext,,}"
  if ! echo "$ext" | grep -qiE "^(${SUPPORTED_EXT})$"; then
    log "SKIP (unsupported): $filename"
    ((skipped++)) || true
    continue
  fi
  
  # Increment count
  count=$((count + 1))
  log "[$count] Processing: $filename ($size bytes)"
  
  # Extract filename without extension for note
  note_basename="${filename%.*}"
  note_file="$VAULT_KNOWLEDGE/${note_basename}.md"
  
  if [[ -f "$note_file" ]]; then
    log "  -> Note already exists, skipping: $note_file"
    ((skipped++)) || true
    continue
  fi
  
  # Copy file to temp
  src_tmp="$TMP_DIR/$filename"
  if [[ "$DRY_RUN" = false ]]; then
    log "  -> Copying file..."
    if ! rclone copy "$REMOTE_PATH/$filename" "$TMP_DIR/" 2>>"$LOG_FILE"; then
      log "  -> ERROR: Failed to copy $filename"
      ((errors++)) || true
      continue
    fi
  else
    log "  -> [DRY RUN] Would copy $REMOTE_PATH/$filename"
  fi
  
  # Extract text
  extracted_file="$TMP_DIR/${note_basename}.extracted.txt"
  if [[ "$DRY_RUN" = false ]]; then
    log "  -> Extracting text..."
    if extract_text "$src_tmp" "$extracted_file"; then
      log "  -> Extraction successful"
    else
      log "  -> Extraction failed or unsupported format"
    fi
  else
    log "  -> [DRY RUN] Would extract text from $filename"
  fi
  
  # Create note
  if [[ "$DRY_RUN" = false ]]; then
    log "  -> Creating knowledge note..."
    create_note "$src_tmp" "$extracted_file" "$note_file"
    log "  -> Note created: $note_file"
    
    # Sync with GBrain (non-blocking)
    log "  -> Syncing vault with GBrain..."
    gbrain sync --repo /root/vault >>"$LOG_FILE" 2>&1 || log "  -> GBrain sync warning"
    
    # Git add and commit (non-blocking)
    log "  -> Adding to git..."
    (
      cd /root/vault
      git add "knowledge/$(basename "$note_file")" 2>/dev/null
      git commit -m "Add knowledge note: $note_basename" 2>/dev/null || true
    ) >>"$LOG_FILE" 2>&1 || true
  else
    log "  -> [DRY RUN] Would create note: $note_file"
  fi
  
  # Cleanup temp file for this iteration
  if [[ "$DRY_RUN" = false ]]; then
    rm -f "$src_tmp" "$extracted_file"
  fi
  
  log "  -> Done: $filename"
done

# Summary
log "=========================================="
log "Ingestion complete"
log "  Processed: $count files"
log "  Skipped:   $skipped files"
log "  Errors:    $errors files"
log "=========================================="

# Final cleanup
if [[ "$DRY_RUN" = false ]]; then
  rm -rf "$TMP_DIR"
  log "Temporary directory cleaned up"
else
  log "[DRY RUN] Temporary directory left at: $TMP_DIR"
fi

log "Done"
