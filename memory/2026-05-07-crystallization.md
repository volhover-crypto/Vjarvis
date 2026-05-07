# 2026-05-07 (вторая часть)

## Сессия: Схемотехника + Gerber + Навыки

### Выполнено:
- Создана принципиальная схема (5 файлов .kicad_sch) — иерархическая структура
- Создан PCB файл с 77 footprint'ами (73 компонента + 4 mounting holes)
- Сгенерированы Gerber файлы (9 слоёв) через pcbnew Python API
- Gerber архив отправлен в Telegram
- Проведён ручной анализ формата KiCad 7.0.11 PCB (gr_line, pad, footprint)
- Установлены: circuit-weaver (22 навыка), book-to-skill
- Создан навык agrometeorology-book (учебник Чиркова)
- Создан навык Dreaming (ретроспективный анализ сессий)
- Установлен и адаптирован find-skills (поиск навыков из ClawHub + Vercel)
- Проведён поиск навыков: agriculture (4 результата), iot (6 результатов)

### Ключевые инсайты:
- KiCad 7.0.11 использует формат PCB v20221018, не v20240108
- gr_line должен иметь stroke и layer как отдельные поля, не inline
- pcbnew Python API изменился: FPID убран, PAD создаётся через FOOTPRINT
- Gerber экспорт через PLOT_CONTROLLER.PlotLayer() работает
- circuit-weaver validate блокирует генерацию из-за строгой валидации YAML
- skidl не работает с KiCad 7 (ищет .lib файлы, а KiCad 7 использует .kicad_sym)

### Проблемы:
- exec preflight блокирует сложные Python-скрипты
- matplotlib конфликтует с numpy 2.x (исправлено downgrade до 1.26.4)
- skidl несовместим с KiCad 7
- FreeRouter не установлен

### Нерешённые:
- Трассировка платы (routing) — требует KiCad GUI или FreeRouter
- DRC проверка
- Copper pour (заполнение медных зон)

### Принципы для будущего:
1. Для генерации KiCad PCB использовать прямую запись в S-expression формате v20221018
2. Для Gerber экспорта использовать pcbnew.PLOT_CONTROLLER + PlotLayer()
3. Для поиска навыков: ClawHub (OpenClaw) + Vercel skills (кросс-платформа)
4. Dreaming-анализ проводить после каждого крупного проекта
