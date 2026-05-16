---
name: mirage-fs
description: Unified virtual filesystem for AI agents via Mirage. Access vault, workspace, and remote services through a single filesystem tree. Use when you need to search, read, copy, or transform data across multiple backends.
---

# Mirage — Unified Virtual Filesystem

Access multiple data sources through a single filesystem tree using familiar bash commands.

## Setup

```python
import asyncio
from mirage import Workspace
from mirage.resource.ram import RAMResource
from mirage.resource.disk import DiskResource
from mirage.resource.github import GitHubResource
from mirage.core.github.config import GitHubConfig

ws = Workspace({
    "/vault": DiskResource(root="/root/vault"),
    "/workspace": DiskResource(root="/root/.openclaw/workspace"),
    "/data": RAMResource(),
    "/github": GitHubResource(
        config=GitHubConfig(token="..."),
        owner="volhover-crypto",
        repo="Vjarvis",
        ref="master"
    ),
})
```

## Common Operations

### Search across all mounts
```bash
# Find all markdown files related to LoRaWAN
grep -r "LoRaWAN" /vault/projects/ --include="*.md"

# Count files by type
find /workspace/skills/ -name "SKILL.md" | wc -l

# Search in specific project
grep -r "энергопотребление" /vault/projects/lorawan-modem/ --include="*.md"
```

### Read files
```bash
# Preview memory
head -30 /workspace/MEMORY.md

# Read full document
cat /vault/projects/agropilot/CONCEPT.md

# Find and read
find /vault/projects/ -name "*.csv" -exec head -5 {} \;
```

### Cross-mount operations
```bash
# Copy from vault to RAM for processing
cp /vault/projects/lorawan-modem/ANALYSIS.md /data/analysis.md

# Process and write back
cat /data/analysis.md | grep "ток" > /data/current.txt
```

### Data analysis
```bash
# Count components in BOM
grep -c "^|" /vault/projects/lorawan-modem/BOM.md

# Extract all references
grep -o 'U[0-9]\+' /vault/projects/lorawan-modem/kicad/lorawan-modem.kicad_sch

# Find large files
find /vault/projects/ -size +1M -exec ls -lh {} \;
```

## Resources

| Mount | Path | Purpose |
|-------|------|---------|
| /vault | /root/vault | Long-term storage, projects |
| /workspace | /root/.openclaw/workspace | Agent skills, memory |
| /data | RAM | Temporary processing |
| /github | GitHub repo | Agent identity backup (Vjarvis) |
| /gdrive | Google Drive | Personal cloud storage |

## Supported Backends

- **DiskResource**: Local filesystem (any path)
- **RAMResource**: In-memory (temporary)
- **S3Resource**: AWS S3, R2, GCS (needs credentials)
- **GitHubResource**: GitHub repos (needs token)
- **SlackResource**: Slack messages (needs token)
- **GDocsResource**: Google Docs (needs OAuth)

## Notes

- Mirage v0.0.1 (beta) — some features may be limited
- Cross-resource copy may not work between disk and RAM
- Commands return `IOResult` with stdout, stderr, exit_code
- Two-layer cache (index + file) for repeated reads
- GitHub resource: owner=volhover-crypto, repo=Vjarvis, ref=master
- GDrive resource: OAuth configured, refresh_token saved
- Use `GITHUB_TOKEN` env var for GitHub authentication
