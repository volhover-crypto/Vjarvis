---
name: claude-bughunter-integration
description: "Claude-BugHunter architecture integration — security testing methodology, 7-Question Gate, red-team discipline, bug bounty workflow, A-to-B chaining, evidence hygiene, reporting. Source: github.com/elementalsouls/Claude-BugHunter (51 skills, 15 commands, 574+ disclosed reports). For adversarial verification and pentest of own infrastructure (mdked.hlab.kz, AgroPilot, n8n, auth system). NOT for external use on third-party targets without authorization."
---

# Claude-BugHunter Architecture Integration

> Интегрировано из: github.com/elementalsouls/Claude-BugHunter
> Источник: 51 skills · 15 slash commands · 574+ disclosed HackerOne reports
> Автор: Sachin Sharma (Bug Hunting & GenAI Security Research)
> Дата интеграции: 2026-05-26

**Область применения:** тестирование СВОИХ систем (mdked.hlab.kz, AgroPilot, n8n, auth service).
**НЕ применять** к сторонним целям без явного разрешения.

---

## 1. Архитектура бандла (4 слоя)

```
Layer 1: МЫШЛЕНИЕ          → bug-bounty + bb-methodology + redteam-mindset
Layer 2: ВЕБ-ПРИЛОЖЕНИЯ     → 27 hunt-* skills + security-arsenal
Layer 3: ENTERPRISE         → m365-entra, okta, cloud-iam, vmware, vpn, sharepoint
Layer 4: ОТЧЁТНОСТЬ         → triage-validation + report-writing + evidence-hygiene
```

**Принцип автозагрузки:** Skills активируются по ключевым словам в описании задачи. Явный вызов не нужен.

---

## 2. 7-Question Gate (triage-validation)

**Применять ДО написания любого отчёта.** Первый FAIL = убить находку.

| # | Вопрос | FAIL = KILL |
|---|--------|-------------|
| Q1 | Могу ли я показать это РЕАЛЬНЫМ HTTP-запросом прямо сейчас? Шаги 1-5 (setup → request → result → impact → cost) | Если нет копипастного запроса → KILL |
| Q2 | Тип импакта в списке принятых программой? | Если exclusions → KILL |
| Q3 | Root cause в in-scope ассете? Не third-party, не staging | Если OOS → KILL |
| Q4 | Требует ли привилегированный доступ, который атакующий нереально получить? | Если "admin only" → KILL |
| Q5 | Не является ли это уже известным / design decision? (Changelog, GitHub issues, docs) | Если acknowledged → KILL |
| Q6 | Конкретный импакт, а не "теоретически возможно"? | Если "could potentially" → KILL |
| Q7 | Не является ли это noise / false positive? | Если soft-404, WAF блокировка → KILL |

**4 входа валидации:** PASS → писать отчёт. DOWNGRADE → переоценить severity. KILL → убрать. CHAIN → сначала построить цепочку.

---

## 3. 5-Phase Hunting Workflow (bb-methodology)

**Нелинейный процесс — фазы можно переключать:**

1. **SCOPE** — определить engagement type (bug bounty / red team / pentest)
2. **RECON** — subdomains, endpoints, JS bundles, identity fabric
3. **HUNT** — систематическое тестирование по классам уязвимостей
4. **VALIDATE** — 7-Question Gate
5. **REPORT** — impact-first отчёт

**НЕ останавливаться** после KILL одной находки — переключаться на следующий класс.

### Developer Psychology Heuristics
- Feature A имеет auth checks → похожий Feature B (новый) — вероятно не имеет
- Сложные флоу (coupon + points + refund) → edge case bugs
- `/api/v2/user` существует → `/api/v1/user` может иметь слабую аутентификацию

### What-If Experiments
- Пропустить checkout → попасть на `/checkout/success` напрямую
- Пропустить 2FA → навигировать на `/dashboard`
- Отправить coupon запрос 10× одновременно → Race condition?
- Заменить `guid=f8a2...` на `id=100` на sibling endpoint → IDOR?

---

## 4. Red Team Discipline (redteam-mindset)

**DO NOT STOP — главная директива:**

- Авторизация дана в начале engagement'а действует до его окончания
- Discipline rules (OOB verification, Marker Discipline, Body-Diff) — это про КОРРЕКТНОСТЬ находок, НЕ про ограничение ЭФФОРТА
- "Stop at PoC" = остановить ЭСКАЛАЦИЮ одного класса, но НЕ остановить ТЕСТИРОВАНИЕ других
- 3000 реквестов через Burp — нормальный cadence для authorized engagement
- Self-throttling anti-patterns — 10 явных паттернов (см. ниже)

### Self-Throttling Anti-Patterns (чеклист)
1. Спрашивать "продолжать?" в процессе, когда user уже выбрал режим
2. Останавливаться на первом 401/403 (есть 12+ auth-bypass классов)
3. "Interesting constant token, not chased" — токен/хеш — это lead, а не artifact
4. Не читать Disallow строки robots.txt
5. Soft-404 (37KB body в 404 status) — читать, grep, diff
6. OpenAPI раскрыт → 4 из N endpoints проверено (проверять ВСЕ)
7. APK retest "deferred — needs tooling" — 5 мин установки jadx
8. Volume как проблема — вопрос в "all test classes on all live surfaces run?"
9. AskUserQuestion в активном loop'е — если режим уже выбран, техническое решение принимается автоматически
10. Skill-gap-as-stop-condition — если hunt-* skill нет, делать вручную по vendor's check matrix

### Complete Sweep Per Live Host
- Top-100 path probe (admin, api, login, /.git, /.env, swagger, openapi.json, /docs, /actuator, robots.txt, sitemap.xml, /.well-known/*)
- robots.txt → каждый Disallow = probe target
- sitemap.xml → каждая запись = probe target
- JS bundles → grep с secret-regex catalogue (Firebase, AWS, GCP, JWT, Stripe, GitHub)
- Source-map paths (*.js.map, /_next/static/*.js.map)
- Каждая форма → SQLi sweep (12+ classes), auth-bypass (12+ classes), CSRF, parameter pollution, mass-assignment, race condition
- Каждый API endpoint → HTTP method tampering, content-type tampering, JWT alg=none, prototype pollution, race conditions
- Identity fabric: GetUserRealm, OpenID well-known, autodiscover-v2, federation behavior

---

## 5. A-to-B Bug Chaining (bug-bounty)

**Один баг платит. Цепочка платит 3-10x.**

| Bug A (Signal) | Hunt for Bug B | Escalate to C |
|---|---|---|
| IDOR (read) | PUT/DELETE на том же endpoint | Full account data manipulation |
| SSRF (any) | Cloud metadata 169.254.169.254 | IAM credential exfil → RCE |
| XSS (stored) | HttpOnly на session cookie? | Session hijack → ATO |
| Open redirect | OAuth redirect_uri accepts your domain | Auth code theft → ATO |
| S3 bucket listing | Enumerate JS bundles | Grep for OAuth client_secret → OAuth chain |
| Rate limit bypass | OTP brute force | Account takeover |
| GraphQL introspection | Missing field-level auth | Mass PII exfil |
| Debug endpoint | Leaked environment variables | Cloud credential → infrastructure access |
| CORS reflects origin | Test with credentials: include | Credentialed data theft |
| Host header injection | Password reset poisoning | ATO via reset link |

**Cluster Hunt Protocol:** 1) Confirm A → 2) Map siblings → 3) Test same class on siblings → 4) Chain to B → 5) Escalate to C → 6) Report chain

---

## 6. OOB-Or-It-Didn't-Happen Gate

**Для blind SSRF / blind XSS / stored XSS — OOB confirmation ОБЯЗАТЕЛЬНА.**

**НЕ является подтверждением:**
- Сервер эхоит URL в error message (string formatting, не outbound request)
- Разный status code для external vs localhost (URL-scheme validator)
- Задержка ответа (DNS resolution в parser'е, не completed fetch)

**Является подтверждением:**
- DNS lookup для уникального Collaborator subdomain в OOB listener
- HTTP request к Collaborator с source IP и User-Agent сервера
- Для JS-контекстов (PDF renderers, headless browsers) — fetch от сервера к callback URL

**Workflow:** Plant Collaborator subdomain (sub-tag per sink) → Send request → Wait 30-120s → Poll listener → Only after confirmed callback claim finding.

---

## 7. Enterprise Attack Surface

### SSL VPN Appliances (enterprise-vpn-attack)
- **Cisco ASA/AnyConnect:** `+CSCOE+/` paths, `webvpn=` cookie
- **Fortinet FortiGate:** `/remote/login`, `SVPNCOOKIE=`
- **Citrix NetScaler/ADC:** `NSC_AAA=` cookie
- **Palo Alto GlobalProtect:** `DSAuthSession=` cookie
- **Pulse Secure/Ivanti:** `DSAuthSession=`
- **F5 Big-IP:** `BIGipServer*` cookie

### M365/Entra ID (m365-entra-attack)
- AADSTS codes: 50034 (user not exist), 50126 (invalid creds), 50053 (locked)
- Smart Lockout math: track attempt counters per user
- ROPC spray → Conditional Access bypass
- OneDrive-based user enumeration (no lockout risk)

### Cloud IAM (cloud-iam-deep)
- AWS: `AKIA` (long-term), `ASIA` (temporary) keys → STS AssumeRole chaining
- Azure: Managed Identity abuse via SSRF, `AccountKey=` storage keys
- GCP: service account JSON → `type: service_account`
- K8s: ServiceAccount token exfil → API server access
- IMDSv1/v2 attacks via SSRF → credential exfil

### VMware vCenter (vmware-vcenter-attack)
- CVE chain: CVE-2021-21972 (vRealize file upload), CVE-2021-21985 (vSAN RCE), CVE-2022-22954 (Workspace ONE SSTI)
- Fingerprint: `/sdk/vimServiceVersions.xml`, `/ui/login`, `/websso/SAML2/Metadata`

---

## 8. Evidence Hygiene (evidence-hygiene)

**Применять ДО любого скриншота / HAR / вложения.**

### Cookie Redaction Protocol
- **Всегда маскировать:** session cookies, csrf-token, Authorization headers, Bearer tokens
- **Можно оставить:** Cloudflare cookies (`__cf_bm`), analytics (`_ga`), trace IDs (`x-datadog-trace-id`)
- **Методы:** DevTools Console PoC (credentials: include) → Preview annotation → jq для HAR

### PII Black-Bar
- **Маскировать:** real names, emails, phones, addresses, profile photos
- **Можно оставить:** usernames, trace IDs, request bodies, response shapes
- **Test account passwords:** acceptable если ротированы после submission

---

## 9. Report Writing (report-writing)

### Title Formula
```
[Bug Class] in [Exact Endpoint/Feature] allows [attacker role] to [impact] [victim scope]
```
Пример: `IDOR in /api/v2/invoices/{id} allows authenticated user to read any customer's invoice data`

### Impact-First Writing
- **НИКОГДА:** "could potentially", "could be used to", "may allow"
- **ВСЕДА:** конкретный HTTP request + конкретный импакт + proof

### CVSS 3.1 Quick Reference
- Critical: Any-user ATO without interaction, RCE, SQLi with data exfil, admin auth bypass
- High: Mass PII exfil, privilege escalation, internal SSRF with data, stored XSS all users
- Medium: IDOR on specific user non-critical data, XSS on sensitive page requiring click
- Low: Non-sensitive info disclosure, clickjacking with PoC

---

## 10. Интеграция с существующей системой

### Связь с Adversarial Verification (SOUL.md)
7-Question Gate → расширение для adversarial verification:
- «Что здесь может пойти не так?» → применять Q1-Q7 к СВОИМ находкам
- «Пользователь получит то, что просил?» → Q1 (real HTTP request proof)
- «Если бы объяснял через аналогию?» → impact-first writing

### Связь с Deviation Rules (SOUL.md)
- Bug found but fails Q1-Q7 → Rule 1 (auto-fix: kill finding, document why)
- Missing OOB verification → Rule 2 (critical: add before reporting)
- Wrong engagement type assumed → Rule 3 (blocking: stop and confirm)

### Связь с Phase-Based Work (HEARTBEAT.md)
- Security audit проекта → использовать 5-Phase Workflow
- Каждая фаза → PLAN.md + SUMMARY.md + VERIFICATION.md
- 7-Question Gate → часть verify фазы

### Практическое применение для своих систем
1. **Аудит mdked.hlab.kz** — SSL/TLS, headers, auth flow, session management
2. **Аудит AgroPilot** — API endpoints, IDOR, auth bypass
3. **Аудит n8n webhook auth** — token validation, rate limiting, injection
4. **Аудит auth service** — bcrypt, session management, SQL injection в raw queries

---

## 11. Что отложить до апгрейда RAM (8GB)

- **Полный GBrain embed** — семантический поиск по всем security findings
- **Автоматизированный scanning** — nuclei, burp suite integration
- **Burp MCP Server** — требует Java + Burp Pro
- **public-skills-builder** — генерация новых hunt-* skills из H1 reports (требует Anthropic API key)
- **cbh CLI** — Python-based CLI для автоматизации (curl-only mode работает и сейчас)

---

## 12. Ключевые файлы и пути

| Что | Путь |
|-----|------|
| Оригинальный репозиторий | `/tmp/Claude-BugHunter/` (clone) |
| Skills | `/tmp/Claude-BugHunter/skills/` (51 директория) |
| Commands | `/tmp/Claude-BugHunter/commands/` (13 файлов) |
| Security Arsenal | `/tmp/Claude-BugHunter/skills/security-arsenal/SKILL.md` |
| Этот навык | `skills/claude-bughunter-integration/SKILL.md` |

---

*Интегрировано: 2026-05-26. Источник: github.com/elementalsouls/Claude-BugHunter*
*Для применения ТОЛЬКО к своим системам (mdked.hlab.kz, AgroPilot, n8n, auth service).*
