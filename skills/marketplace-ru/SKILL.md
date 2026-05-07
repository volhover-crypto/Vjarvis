---
name: marketplace-ru
description: >
  Use when managing orders, prices, or inventory on Russian e-commerce marketplaces:
  Ozon, Wildberries, Yandex Market. Triggers on mentions of marketplace orders,
  seller API, stock management, price updates, order status, shipping deadlines,
  mp-orders, mp-prices, mp-stocks, or any Ozon/WB/YM seller operations. Always use
  this skill when the user mentions marketplace management, even if they don't
  specify which platform.
---

# Marketplace RU — Ozon / Wildberries / Яндекс Маркет

Управление заказами, ценами и остатками на российских маркетплейсах.

## Platforms

| Платформа | Флаг | API | Особенности |
|-----------|------|-----|-------------|
| Ozon | `--platform ozon` (по умолчанию) | Seller API v3/v4 | FBS/FBO |
| Wildberries | `--platform wb` | Wildberries API | Dual status, цены в копейках, 409=10x penalty |
| Яндекс Маркет | `--platform ymarket` | Partner API | Карантин цен, 100+ субстатусов, rate limit 420 |

## Preflight

Before any operation, check if tools are available and credentials are configured:

```bash
which mp-orders mp-prices mp-stocks mp-setup mp-test
mp-test --platform ozon
```

If tools are not in PATH, add them:
```bash
export PATH="<skill-directory>/tools:$PATH"
```

## Authentication

Each platform requires its own API credentials.

### Ozon
1. [Ozon Seller](https://seller.ozon.ru/) → Настройки → API ключи
2. Create key with **Admin** or **Content + Analytics** permissions
3. Run `mp-setup --platform ozon` — enter Client ID and API Key

### Wildberries
1. [WB Seller](https://seller.wildberries.ru/) → Настройки → API токены
2. Create token with categories: **Marketplace**, **Content**, **Analytics**
3. Run `mp-setup --platform wb` — enter API Token

> Different WB endpoints require tokens from different categories. One token with all needed categories covers all operations.

### Яндекс Маркет
1. [YM Partner](https://partner.market.yandex.ru/) → Настройки → API и модули
2. Create token (max 30 per account)
3. Run `mp-setup --platform ymarket` — enter API Key

> Scope changes take ~10 minutes to propagate. Business ID and Campaign ID are detected automatically on first connection.

### Verify connection
```bash
mp-test --platform ozon
mp-test --platform wb
mp-test --platform ymarket
```

## Orders

```bash
# List orders
mp-orders list --platform ozon
mp-orders list --platform wb
mp-orders list --platform ymarket

# Order status
mp-orders status 12345678-0001-1                    # Ozon: posting number
mp-orders status 987654321 --platform wb             # WB: numeric ID
mp-orders status 77001122 --platform ymarket         # YM: order ID

# Statistics
mp-orders stats --platform wb

# Mock mode (no real API calls)
mp-orders list --mock
```

**Platform-specific behavior:**
- **WB**: Dual status model (supplierStatus + wbStatus), prices in kopecks
- **YM**: 100+ substatus values, ISO dates with timezone

## Prices

```bash
# Get price
mp-prices get TWS-PRO-001
mp-prices get 12345678 --platform wb              # WB: nmID (number)
mp-prices get TWS-PRO-001 --platform ymarket

# Update price (with confirmation)
mp-prices update TWS-PRO-001 2500
mp-prices update 12345678 1999 --platform wb      # enter in rubles, auto-converts to kopecks
mp-prices update TWS-PRO-001 2500 --platform ymarket

# With old price (Ozon: crossed-out price)
mp-prices update TWS-PRO-001 2500 --old-price 2999

# Auto-confirm (only for changes ≤50%)
mp-prices update TWS-PRO-001 2500 --yes

# List all prices
mp-prices list --platform wb

# Yandex Market: price quarantine (on change >5%)
mp-prices confirm-quarantine --platform ymarket
```

**Price change protection:**
- Changes > ±50% require additional confirmation
- `--yes` does not work for changes > 50% (use `--force`)
- Price cannot be 0

**Platform-specific:**
- **WB**: Prices stored in kopecks. Enter in rubles — conversion is automatic.
- **YM**: After price update, quarantine is checked automatically. Changes >5% may be held. Use `confirm-quarantine` to approve.
- **YM**: Currency in API is `RUR` (not `RUB`).

## Stocks

```bash
# All stocks
mp-stocks list
mp-stocks list --platform wb
mp-stocks list --platform ymarket

# Low stock items
mp-stocks list --low                        # < 10 units (default)
mp-stocks list --low --threshold 5          # < 5 units

# Specific item
mp-stocks get TWS-PRO-001

# Update stock
mp-stocks update TWS-PRO-001 100
mp-stocks update 2000000000011 50 --platform wb --warehouse 507921
mp-stocks update TWS-PRO-001 100 --platform ymarket
```

**Platform-specific:**
- **WB**: Stock is warehouse-bound. Use `--warehouse <id>`. Warehouse list is cached automatically.
- **YM**: SKU is case-sensitive and padding-sensitive (`"557722" ≠ "0557722"`). Max 2000 SKUs per request.

## Audit Log & Rollback

All price and stock changes are recorded:

```bash
# Change history
mp-prices history                              # last 20 entries
mp-prices history --sku TWS-PRO-001            # history for SKU
mp-stocks history                              # stock history

# Rollback
mp-prices rollback --last                      # rollback last batch
mp-prices rollback 20260216-143022-a1b2c3d4    # by specific ID
mp-stocks rollback --last --mock               # test in mock mode
```

Rollback always requires manual confirmation. Cannot rollback a rollback (cycle protection). Entries older than 90 days are rotated automatically.

## Error Handling

| Code | Ozon | WB | YM |
|------|------|----|----|
| Rate limit | 429 | 429 (+ 409=10x) | **420** (not 429!) |
| Auth | 401/403 | 401/403 | 401/403 |
| Not found | 404 | 404 | 404 (check businessId/campaignId!) |

Rate limiting: automatic retry with exponential backoff (5s → 15s → 30s).

## Batch Operations

Bulk updates are automatically chunked:
- Chunk size: 10 (configurable via `BATCH_SIZE`)
- Delay: 1 second between chunks (`BATCH_DELAY`)
- Progress: `[30/100] Processing... ETA: 7s`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Credentials not configured | `mp-setup --platform <ozon\|wb\|ymarket>` |
| 401 — invalid credentials | Recreate key in marketplace dashboard, run `mp-setup` again |
| 403 — access denied | Check token permissions/categories (WB) or scope (YM) |
| 429/420 — rate limit | Auto-retry handles this; if persistent, wait 60s |
| `jq: command not found` | `brew install jq` (macOS) or `apt install jq` (Linux) |

## API Documentation

- [Ozon Seller API](https://docs.ozon.ru/api/seller/)
- [Wildberries API](https://openapi.wildberries.ru/)
- [Яндекс Маркет Partner API](https://yandex.ru/dev/market/partner-api/)
