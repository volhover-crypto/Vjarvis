# marketplace-ru

Управление заказами, ценами и остатками на Ozon, Wildberries и Яндекс Маркете через AI-агента.

## Платформы

| Платформа | Заказы | Цены | Остатки | Особенности |
|-----------|--------|------|---------|-------------|
| **Ozon** | FBS/FBO | Рубли | По складам | Seller API v3/v4 |
| **Wildberries** | FBS | Копейки → рубли | По складам | Dual status, 409=10x penalty |
| **Яндекс Маркет** | FBS | Рубли (RUR) | По кампаниям | Карантин цен, 100+ субстатусов |

## Быстрый старт

```bash
# Настройка (по одному для каждой площадки)
mp-setup --platform ozon
mp-setup --platform wb
mp-setup --platform ymarket

# Проверка подключения
mp-test --platform ozon
```

Credentials хранятся в `~/.openclaw/marketplace/*.env` с правами 0600.

## Использование

```bash
# Заказы
mp-orders list --platform wb

# Цены (с подтверждением, валидацией ±50%, rollback)
mp-prices get TWS-PRO-001
mp-prices update TWS-PRO-001 2500

# Остатки
mp-stocks list --low --platform ymarket
```

Все команды принимают `--platform ozon|wb|ymarket` и `--mock` для тестирования.

## Требования

- **jq**, **curl**, **bash** 3.2+

## Подводные камни

- **WB:** код 409 считается за 10 запросов к лимиту
- **WB:** для обновления остатков обязателен `--warehouse <id>`
- **Яндекс Маркет:** использует код 420 (не 429) для rate limit
- **Яндекс Маркет:** изменения scope токена вступают в силу через ~10 минут
- **Яндекс Маркет:** SKU чувствителен к регистру

Подробная документация — в [SKILL.md](./SKILL.md).
