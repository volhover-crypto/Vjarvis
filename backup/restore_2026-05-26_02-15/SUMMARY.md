# Точка восстановления — 2026-05-26 02:15 (Almaty)

## Состояние системы

### Сервисы
| Сервис | Статус | Порт |
|--------|--------|------|
| OpenClaw Gateway | ✅ running | 18789 (loopback) |
| n8n | ✅ Up | 5678 |
| PostgreSQL 16 | ✅ active | 5432 (loopback) |
| NGINX | ✅ active | 80, 443 |
| Docker | ✅ active | — |
| Syncthing | ✅ running | 8384 (loopback) |
| jarvis-auth (FastAPI) | ✅ running | 8765 |
| auth proxy (python) | ✅ running | 8080 (loopback only) |
| Xray | ✅ running | 10808/10809 (loopback) |
| GBrain | ❌ FAILED | — (SIGKILL, отложено до RAM 8GB) |
| certbot | ❌ FAILED | — (SSL валиден до 2026-08-17) |
| tuned | ❌ disabled | — (отключен как бесполезный на VPS) |

### Ресурсы
| Метрика | Значение |
|---------|----------|
| RAM | 1.8GB total, 487MB available, 1.3GB used |
| Swap | 2.9GB total (zram 921MB + swapfile 2GB), 810MB used |
| vm.swappiness | 10 |
| Disk | 75% (28G/40G), 9.5GB free |
| Inodes | 29% used |
| Load | 0.06 / 0.03 / 0.08 |
| Uptime | 55 days |

### Топ процессы по RAM
1. OpenClaw Gateway (node) — 454MB (24.6%)
2. n8n (node) — 210MB (11.4%)
3. n8n task-runner (node) — 69MB (3.7%)
4. dockerd — 23MB (1.2%)
5. syncthing — 17MB (0.9%)
6. xray — 15MB (0.8%)
7. containerd — 15MB (0.8%)
8. snapd — 15MB (0.8%)
9. systemd-journald — 14MB (0.7%)
10. auth proxy (python) — 8MB (0.4%)
11. jarvis-auth (python) — 7MB (0.3%)

### Внешние порты (0.0.0.0)
- 22 (SSH)
- 80 (nginx)
- 443 (nginx)
- 5678 (n8n)
- 8765 (jarvis-auth)

### Loopback-only порты
- 5432 (PostgreSQL)
- 18789 (OpenClaw)
- 8384 (Syncthing)
- 8080 (auth proxy)
- 10808/10809 (Xray)

### NGINX конфигурация
- worker_connections: 4096
- TLS: 1.2+ only (1.0/1.1 отключены)
- server_tokens: off
- Sites-enabled: coach (145 lines)
- Let's Encrypt: до 2026-08-17

### Размеры директорий
- Vault: 164MB
- .openclaw: 2.1GB
- Workspace: ~459MB
- /tmp: 387MB
- /var/log: 113MB
- Docker images: 2.52GB (n8n 2.27GB, python 179MB, alpine 13MB)
- Docker volumes: 1.079GB (99% reclaimable)

### Крупные файлы
- /swapfile: 2GB
- /usr/local/bin/gbrain: бинари
- /root/.cache/whisper/tiny.pt, small.pt: whisper модели
- Whisper tiny (39MB), small (150MB), medium (466MB), large (1.5GB), turbo (1.6GB)

### Git
- Repo: volhover-crypto/Vjarvis (master)
- Коммиты: 8+
- Последний: 5195113 (optimize: full system audit + hardening)

### Cron / Scheduled
| Задача | Расписание |
|--------|-----------|
| Memory Crystallizer | ежедневно 2:00 |
| arXiv search | пн 9:00 |
| AI Coach parser | каждые 30 мин |
| FreeLLMAPI reminder | пн 10:00 |

### Навыки
- Всего: 57
- Новый (05-26): claude-bughunter-integration

### Ключевые события сессии
1. Кристаллизация состояния (01:24)
2. Восстановление NGINX (01:30) — убиты старые процессы, перезапуск
3. Оптимизация системы (01:39):
   - Убит gbrain zombie (97.6% CPU)
   - Journal vacuum: 268MB → 70MB
   - tuned disabled
   - qemu-ga killed
   - Порт 8080 → 127.0.0.1 (security)
   - nginx: TLS 1.2+, worker_connections 4096, server_tokens off
   - vm.swappiness: 10

### Отложено до апгрейда (RAM 8GB, диск +500MB)
- GBrain embed (1579 чанков)
- Автоматизированный scanning
- certbot repair
- Docker volume cleanup
