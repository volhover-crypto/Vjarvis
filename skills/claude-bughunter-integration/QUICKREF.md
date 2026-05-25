# BugHunter Quick Reference

## 7-Question Gate (до любого отчёта)
Q1: Real HTTP request? → Q2: Accepted impact? → Q3: In-scope? → Q4: No privileged access? → Q5: Not known? → Q6: Concrete impact? → Q7: Not noise?
**Первый NO = KILL. Не останавливать engagement, убрать находку, идти дальше.**

## A→B Chaining (после каждой находки)
IDOR → PUT/DELETE → data manipulation
SSRF → cloud metadata → IAM creds → RCE
XSS → cookie theft → ATO
Open redirect → OAuth theft → ATO
Rate limit bypass → OTP brute → ATO

## Red Team Discipline
- DO NOT STOP после первой защиты (401/403/WAF)
- 12+ auth-bypass классов на каждый surface
- Каждый Disallow в robots.txt — probe target
- Каждый endpoint в OpenAPI — все test classes
- OOB confirmation для blind vulns (всегда)

## OOB Gate
- Echo в error message ≠ SSRF/XSS
- Status code diff ≠ SSRF
- Collaborator DNS+HTTP callback = подтверждение
- Sub-tag по sink (параметру) для точной атрибуции

## Report Writing
Title: `[Bug Class] in [Endpoint] allows [role] to [impact] [scope]`
Никогда: "could potentially" / "may allow" / "could be used to"
Всегда: конкретный HTTP request + конкретный импакт + PoC

## Свои системы для аудита
1. mdked.hlab.kz — headers, TLS, auth flow
2. AgroPilot — API, IDOR, auth bypass
3. n8n webhook — token validation, rate limiting
4. auth service — bcrypt, sessions, SQL injection
