#!/bin/bash

# skills/crystallizer/scripts/crystallizer.sh
# Скрипт навыка crystallizer: Knowledge Crystallization Cycle (NFD + EvolveR)
# Часть навыка OpenClaw: skills/crystallizer/
# Выполняется в Surgical Workspace (Claude Code, n8n, локальный редактор)
# как batch-операция по триггеру или расписанию.

set -euo pipefail

# Конфигурация: пути к ключевым файлам и директориям
WORKSPACE_ROOT="/root/.openclaw/workspace"
MEMORY_DIR="${WORKSPACE_ROOT}/memory"
PRINCIPLES_LIB="${MEMORY_DIR}/principles_lib.md"
MEMORY_SUMMARY="${WORKSPACE_ROOT}/MEMORY.md"
PLANS_DIR="${WORKSPACE_ROOT}/plans"
SKILLS_DIR="${WORKSPACE_ROOT}/skills"

# Время запуска для отчёта и имён файлов
START_TIME=$(date '+%Y-%m-%d %H:%M:%S')
TIMESTAMP_FILE=$(date '+%Y-%m-%d_%H-%M-%S')

# Временная директория для обработки
TMP_DIR=$(mktemp -d)
trap 'rm -rf "${TMP_DIR}"' EXIT

# Лог-файл для отладки (опционально)
LOG_FILE="${TMP_DIR}/crystallizer.log"

# Функция для логирования (в файл и в stderr)
log() {
    echo "[$(date '+%H:%M:%S')] $*" | tee -a "${LOG_FILE}" >&2
}

log "=== Запуск навыка crystallizer: Knowledge Crystallization Cycle ==="
log "Время запуска: ${START_TIME}"
log "Рабочая директория: ${WORKSPACE_ROOT}"
# Проверка существования ключевых директорий и файлов
log "Проверка существования ключевых путей..."

# Директории
for dir in "${MEMORY_DIR}" "${PLANS_DIR}" "${SKILLS_DIR}"; do
    if [ ! -d "${dir}" ]; then
        log "ОШИБКА: Директория не существует: ${dir}"
        exit 1
    fi
done

# Файлы
for file in "${PRINCIPLES_LIB}" "${MEMORY_SUMMARY}"; do
    if [ ! -f "${file}" ]; then
        log "Предупреждение: файл не существует, будет создан: ${file}"
        touch "${file}"
    fi
done

# Проверяем поддиректории skills/*/references/
log "Проверка структуры навыков..."
if [ ! -d "${SKILLS_DIR}" ]; then
    log "ОШИБКА: Директория навыков не существует: ${SKILLS_DIR}"
    exit 1
fi

# Считаем количество навыков с references/
SKILL_COUNT=0
for skill_dir in "${SKILLS_DIR}"/*/; do
    if [ -d "${skill_dir}" ] && [ -d "${skill_dir}references/" ]; then
        SKILL_COUNT=$((SKILL_COUNT + 1))
    fi
done

log "Найдено навыков с references/: ${SKILL_COUNT}"
if [ "${SKILL_COUNT}" -eq 0 ]; then
    log "Предупреждение: не найдено навыков с директорией references/ — кристаллизация всё равно продолжит работу, но не будет знать, куда записывать принципы"
fi

log "Проверка путей завершена."

# Сбор всех записей опыта из memory/ для обработки
log "Сбор записей опыта из memory/..."

# Временной файл для всех собранных записей
ALL_RECORDS="${TMP_DIR}/all_records.md"
> "${ALL_RECORDS}"  # Очистить или создать пустой файл

# 1. Собрать все дневные логи (memory/YYYY-MM-DD.md)
log "Сбор записей из дневных логов (memory/YYYY-MM-DD.md)..."
if ls "${MEMORY_DIR}"/*.md 1>/dev/null 2>&1; then
    for log_file in "${MEMORY_DIR}"/*.md; do
        # Пропускаем principles_lib.md и error_patterns.md из основного потока
        basename=$(basename "${log_file}")
        if [ "${basename}" = "principles_lib.md" ] || [ "${basename}" = "error_patterns.md" ]; then
            log "Пропускаем служебный файл из основного потока: ${basename}"
            continue
        fi
        log "Обрабатываем файл: ${basename}"
        # Извлекаем все строки, которые выглядят как заголовки записей и их содержимое
        # Упрощённый подход: берём блоки между ## [TAG] HH:MM — и следующим ## [TAG] или концом файла
        # Для простоты в этой версии будем извлекать строки, содержащие теги в квадратных скобках
        grep -E '^## \[(OPERATIONAL_RECORD|INSIGHT|ERROR|PATTERN|DECISION|CASE)\]' "${log_file}" >> "${ALL_RECORDS}" 2>/dev/null || true
        # Также извлечём несколько следующих строк после каждого заголовка, чтобы получить содержимое записи
        # Это упрощённый подход — в будущем можно улучшить парсинг
        grep -A 10 -E '^## \[(OPERATIONAL_RECORD|INSIGHT|ERROR|PATTERN|DECISION|CASE)\]' "${log_file}" >> "${ALL_RECORDS}" 2>/dev/null || true
        echo "" >> "${ALL_RECORDS}"  # Разделитель между файлами
    done
else
    log "Предупреждение: дневные логи не найдены в ${MEMORY_DIR}"
fi

# 2. Собрать записи из error_patterns.md (как источник ошибок)
log "Сбор записей из error_patterns.md..."
if [ -f "${MEMORY_DIR}/error_patterns.md" ]; then
    grep -E '^## \[ERROR\]' "${MEMORY_DIR}/error_patterns.md" >> "${ALL_RECORDS}" 2>/dev/null || true
    grep -A 10 -E '^## \[ERROR\]' "${MEMORY_DIR}/error_patterns.md" >> "${ALL_RECORDS}" 2>/dev/null || true
    echo "" >> "${ALL_RECORDS}"
else
    log "Предупреждение: файл error_patterns.md не найден"
fi

# 3. Собрать записи из каталога cases/ (если есть)
log "Сбор записей из memory/cases/..."
if [ -d "${MEMORY_DIR}/cases/" ] && ls "${MEMORY_DIR}/cases/"/* 1>/dev/null 2>&1; then
    for case_file in "${MEMORY_DIR}/cases/"/*; do
        if [ -f "${case_file}" ]; then
            basename=$(basename "${case_file}")
            log "Обрабатываем кейс: ${basename}"
            grep -E '^## \[(OPERATIONAL_RECORD|INSIGHT|ERROR|PATTERN|DECISION|CASE)\]' "${case_file}" >> "${ALL_RECORDS}" 2>/dev/null || true
            grep -A 10 -E '^## \[(OPERATIONAL_RECORD|INSIGHT|ERROR|PATTERN|DECISION|CASE)\]' "${case_file}" >> "${ALL_RECORDS}" 2>/dev/null || true
            echo "" >> "${ALL_RECORDS}"
        fi
    done
else
    log "Предупреждение: каталог memory/cases/ пуст или не существует"
fi

# Подсчитаем количество потенциальных записей
RECORD_COUNT=$(grep -c '^## \[(OPERATIONAL_RECORD|INSIGHT|ERROR|PATTERN|DECISION|CASE)\]' "${ALL_RECORDS}" 2>/dev/null || echo 0)
log "Собрано потенциальных записей для обработки: ${RECORD_COUNT}"

if [ "${RECORD_COUNT}" -eq 0 ]; then
    log "ОШИБКА: Не найдено записей для обработки. Кристаллизация невозможна."
    exit 1
fi

log "Сбор записей завершён."

# Группировка записей по тегам и извлечение повторяющихся паттернов
log "Группировка записей по тегам и поиск повторяющихся паттернов..."

# Временная директория для обработки по тегам
TAG_DIR="${TMP_DIR}/by_tag"
mkdir -p "${TAG_DIR}"

# Список тегов для обработки
TAGS="OPERATIONAL_RECORD INSIGHT ERROR PATTERN DECISION CASE"

# Обходим каждый тег
for TAG in ${TAGS}; do
    log "Обработка тега: [${TAG}]"
    
    # Извлекаем все блоки записей с данным тегом
    # Упрощённый подход: ищем строки, начинающиеся с ## [TAG] HH:MM — и берём их и несколько следующих строк
    TAG_FILE="${TAG_DIR}/${TAG}.md"
    > "${TAG_FILE}"
    
    # Используем awk для извлечения блоков: начинается с ## [TAG] ... и продолжается до следующего ## [TAG] или конца файла
    awk "
    BEGIN { in_block = 0; block_lines = 0; max_lines = 12 }
    /^## \\[${TAG}\\]/ {
        if (in_block == 1) {
            print block_content
        }
        in_block = 1
        block_lines = 0
        block_content = \$0 \"\\n\"
        next
    }
    /^## \[(OPERATIONAL_RECORD|INSIGHT|ERROR|PATTERN|DECISION|CASE)\]/ {
        if (in_block == 1 && block_lines > 0) {
            print block_content
        }
        in_block = 0
        next
    }
    {
        if (in_block == 1) {
            if (block_lines < max_lines) {
                block_content = block_content \$0 \"\\n\"
                block_lines++
            }
        }
    }
    END {
        if (in_block == 1 && block_lines > 0) {
            print block_content
        }
    }
    " "${ALL_RECORDS}" > "${TAG_FILE}" 2>/dev/null || true
    
    # Подсчитаем количество записей с этим тегом
    TAG_COUNT=$(grep -c '^## \\['"${TAG}"'\\]' "${TAG_FILE}" 2>/dev/null || echo 0)
    log "Найдено записей с тегом [${TAG}]: ${TAG_COUNT}"
    
    # Если записей меньше 3 — паттернов не может быть по условию ≥3
    if [ "${TAG_COUNT}" -lt 3 ]; then
        log "Записей с тегом [${TAG}] меньше 3 — переход к следующему тегу"
        continue
    fi
    
    # Извлечём ключевые поля из записей этого тега для поиска паттернов
    # Мы будем искать повторяющиеся фразы в:
    # - Задаче
    # - Что сработало
    # - Что не сработало
    # - Чего не хватало
    # - Принципе для будущего
    
    # Временные файлы для полей
    FIELD_TASK="${TAG_DIR}/${TAG}_task.txt"
    FIELD_WENT_WELL="${TAG_DIR}/${TAG}_went_well.txt"
    FIELD_WENT_WRONG="${TAG_DIR}/${TAG}_went_wrong.txt"
    FIELD_MISSING="${TAG_DIR}/${TAG}_missing.txt"
    FIELD_PRINCIPLE="${TAG_DIR}/${TAG}_principle.txt"
    
    > "${FIELD_TASK}"
    > "${FIELD_WENT_WELL}"
    > "${FIELD_WENT_WRONG}"
    > "${FIELD_MISSING}"
    > "${FIELD_PRINCIPLE}"
    
    # Извлечём содержимое полей из каждой записи
    # Упрощённый парсер: ищем строки, начинающиеся с **Поле**: и берём содержимое до следующего **Поле**: или пустой строки
    # Это не идеально, но работает для чётко отформатированных записей
    
    awk "
    BEGIN { 
        field = \"none\"; 
        in_field = 0; 
        collecting = 0
        task = \"\"; went_well = \"\"; went_wrong = \"\"; missing = \"\"; principle = \"\"
    }
    /^## \\[${TAG}\\]/ {
        # Начало новой записи — сбрасываем накопители
        if (task != \"\") {
            print task > \"'"${FIELD_TASK}"'\"
            print went_well > \"'"${FIELD_WENT_WELL}"'\"
            print went_wrong > \"'"${FIELD_WENT_WRONG}"'\"
            print missing > \"'"${FIELD_MISSING}"'\"
            print principle > \"'"${FIELD_PRINCIPLE}"'\"
            task = \"\"; went_well = \"\"; went_wrong = \"\"; missing = \"\"; principle = \"\"
        }
        field = \"none\"; in_field = 0; collecting = 0
        next
    }
    /^\*\*Задача\*\*:/ {
        field = \"task\"; in_field = 1; collecting = 1
        sub(/^\*\*Задача\*\*: /, \"\")
        task = \$0
        next
    }
    /^\*\*Что сработало\*\*:/ {
        field = \"went_well\"; in_field = 1; collecting = 1
        sub(/^\*\*Что сработало\*\*: /, \"\")
        went_well = \$0
        next
    }
    /^\*\*Что не сработало\*\*:/ {
        field = \"went_wrong\"; in_field = 1; collecting = 1
        sub(/^\*\*Что не сработало\*\*: /, \"\")
        went_wrong = \$0
        next
    }
    /^\*\*Чего не хватало\*\*:/ {
        field = \"missing\"; in_field = 1; collecting = 1
        sub(/^\*\*Чего не хватало\*\*: /, \"\")
        missing = \$0
        next
    }
    /^\*\*Принцип для будущего\*\*:/ {
        field = \"principle\"; in_field = 1; collecting = 1
        sub(/^\*\*Принцип для будущего\*\*: /, \"\")
        principle = \$0
        next
    }
    /^$/ || /^## \[/ {
        # Конец поля при пустой строке или начале новой записи
        if (in_field == 1 && collecting == 1) {
            if (field == \"task\") {
                print task > \"'"${FIELD_TASK}"'\"
            } else if (field == \"went_well\") {
                print went_well > \"'"${FIELD_WENT_WELL}"'\"
            } else if (field == \"went_wrong\") {
                print went_wrong > \"'"${FIELD_WENT_WRONG}"'\"
            } else if (field == \"missing\") {
                print missing > \"'"${FIELD_MISSING}"'\"
            } else if (field == \"principle\") {
                print principle > \"'"${FIELD_PRINCIPLE}"'\"
            }
            in_field = 0
            collecting = 0
            task = \"\"; went_well = \"\"; went_wrong = \"\"; missing = \"\"; principle = \"\"
        }
        next
    }
    {
        if (in_field == 1 && collecting == 1) {
            if (field == \"task\") {
                task = task \" \" \$0
            } else if (field == \"went_well\") {
                went_well = went_well \" \" \$0
            } else if (field == \"went_wrong\") {
                went_wrong = went_wrong \" \" \$0
            } else if (field == \"missing\") {
                missing = missing \" \" \$0
            } else if (field == \"principle\") {
                principle = principle \" \" \$0
            }
        }
    }
    END {
        # Выводим последнюю накопленную запись, если есть
        if (task != \"\" || went_well != \"\" || went_wrong != \"\" || missing != \"\" || principle != \"\") {
            print task > \"'"${FIELD_TASK}"'\"
            print went_well > \"'"${FIELD_WENT_WELL}"'\"
            print went_wrong > \"'"${FIELD_WENT_WRONG}"'\"
            print missing > \"'"${FIELD_MISSING}"'\"
            print principle > \"'"${FIELD_PRINCIPLE}"'\"
        }
    }
    " "${TAG_FILE}" > /dev/null 2>&1 || true
    
    # Теперь ищем повторяющиеся фразы в каждом поле (минимум 3 совпадения)
    log "Поиск повторяющихся фраз в полях для тега [${TAG}]..."
    
    # Временной файл для найденных паттернов этого тега
    PATTERNS_FOUND="${TAG_DIR}/${TAG}_patterns.txt"
    > "${PATTERNS_FOUND}"
    
    # Функция для поиска фраз, встречающихся минимум min_count раз
    find_repeating_phrases() {
        local field_file="$1"
        local field_name="$2"
        local min_count=3
        
        if [ ! -s "${field_file}" ]; then
            log "  Предупреждение: файл поля пуст: ${field_file}"
            return
        fi
        
        log "  Анализ поля: ${field_name} (мин. совпадений: ${min_count})"
        
        # Удаляем пустые строки и приводим к нижнему регистру для поиска (но сохраняем оригинал для вывода)
        # Сортируем, считаем уникальные, фильтруем по счётчику >= min_count
        sort "${field_file}" | uniq -c | awk -v min="${min_count}" '$1 >= min {print $0}' | while read -r count line; do
            # Убираем ведущий счётчик и лишние пробелы
            phrase=$(echo "${line}" | sed 's/^[[:space:]]*[0-9][[:space:]]*//')
            if [ -n "${phrase}" ]; then
                echo "Найден паттерн в поле ${field_name} (${match_count} совпадений): \"${phrase}\"" >> "${PATTERNS_FOUND}"
                log "    Найден паттерн в поле ${field_name}: \"${phrase}\" (${count} совпадений)"
            fi
        done
    }
    
    # Применяем функцию к каждому полю
    find_repeating_phrases "${FIELD_TASK}" "Задача"
    find_repeating_phrases "${FIELD_WENT_WELL}" "Что сработало"
    find_repeating_phrases "${FIELD_WENT_WRONG}" "Что не сработало"
    find_repeating_phrases "${FIELD_MISSING}" "Чего не хватало"
    find_repeating_phrases "${FIELD_PRINCIPLE}" "Принцип для будущего"
    
    # Подсчитаем общее количество найденных паттернов для этого тега
    TAG_PATTERN_COUNT=$(wc -l < "${PATTERNS_FOUND}" 2>/dev/null || echo 0)
    log "Найдено паттернов для тега [${TAG}]: ${TAG_PATTERN_COUNT}"
    
    # Если паттернов нет — переход к следующему тегу
    if [ "${TAG_PATTERN_COUNT}" -eq 0 ]; then
        log "Паттернов не найдено для тега [${TAG}] — переход к следующему тегу"
        continue
    fi
    
    # Для каждого найденного паттерна попробуем сформулировать обобщённый принцип
    log "Формулирование обобщённых принципов для тега [${TAG}]..."
    
    # Временной файл для принципов этого тега
    TAG_PRINCIPLES="${TAG_DIR}/${TAG}_principles.txt"
    > "${TAG_PRINCIPLES}"
    
    # Читаем каждый найденный паттерн и пытаемся сформулировать принцип
    while IFS= read -r pattern_line; do
        # Извлекаем саму фразу из строки типа:
        # "Найден паттерн в поле Что сработало (5 совпадений): \"запуск анализа данных датчика\""
        if [[ "${pattern_line}" =~ Найден\ паттерн\ в\ поле\ ([^)]+)\ \(([0-9]+)\ совпадений\):\ \"(.+)\" ]]; then
            field_match="${BASH_REMATCH[1]}"
            count_match="${BASH_REMATCH[2]}"
            phrase_match="${BASH_REMATCH[3]}"
            
            # Формулируем обобщённый принцип на основе поля и фразы
            # Это упрощённый де-контекстуализатор
            principle_suggestion=""
            case "${field_match}" in
                "Задача")
                    principle_suggestion="При выполнении задач подобного типа следует уделять особое внимание контексту и проверять исходные данные."
                    ;;
                "Что сработало")
                    principle_suggestion="Метод, доказавший свою эффективность в подобных ситуациях, следует рассматривать как кандидат для стандартизации."
                    ;;
                "Что не сработало")
                    principle_suggestion="Подход, показавший низкую эффективность в подобных контекстах, требует пересмотра или замены на альтернативные методы."
                    ;;
                "Чего не хватало")
                    principle_suggestion="При планировании подобных задач необходимо заранее обеспечивать доступ к указанным ресурсам, данным или знаниям."
                    ;;
                "Принцип для будущего")
                    principle_suggestion="${phrase_match}"  # Уже почти принцип — просто проверяем формат
                    ;;
                *)
                    principle_suggestion="При работе с задачами, связанными с ${field_match}, следует учитывать выявленные закономерности и адаптировать подход соответственно."
                    ;;
            esac
            
            # Добавляем в список принципов этого тега
            echo "Принцип (из поля ${field_match}, ${count_match} совпадений): ${principle_suggestion}" >> "${TAG_PRINCIPLES}"
            log "  Сформулирован принцип: ${principle_suggestion}"
            
        else
            log "Предупреждение: не удалось распарсить строку паттерна: ${pattern_line}"
        fi
    done < "${PATTERNS_FOUND}"
    
    # Подсчитаем количество сформулированных принципов для этого тега
    TAG_PRINCIPLE_COUNT=$(wc -l < "${TAG_PRINCIPLES}" 2>/dev/null || echo 0)
    log "Сформулировано принципов для тега [${TAG}]: ${TAG_PRINCIPLE_COUNT}"
    
    # Сохраняем результаты этого тега для дальнейшей обработки
    # В реальной версии здесь бы был переход к проверке дублирования и валидации
    # Мы просто аккумулируем всё в общий поток
    
    cat "${TAG_PRINCIPLES}" >> "${TMP_DIR}/all_principles_to_check.md" 2>/dev/null || true
    echo "" >> "${TMP_DIR}/all_principles_to_check.md"
    
done

# Подсчитаем общее количество сформулированных принципов
TOTAL_PRINCIPLE_COUNT=$(wc -l < "${TMP_DIR}/all_principles_to_check.md" 2>/dev/null || echo 0)
log "Всего сформулировано принципов для проверки: ${TOTAL_PRINCIPLE_COUNT}"

if [ "${TOTAL_PRINCIPLE_COUNT}" -eq 0 ]; then
    log "ОШИБКА: Не сформулировано ни одного принципа для проверки. Возможно, недостаточно данных или слишком строгие критерии."
    log "Совет: увеличьте объём данных или уменьшите порог для поиска паттернов (например: с 3 до 2 совпадений) для тестирования."
    exit 1
fi

log "Группировка по тегам и извлечение паттернов завершён."

# Проверка сформулированных принципов на дублирование в библиотеке принципов
log "Проверка принципов на дублирование в ${PRINCIPLES_LIB}..."

# Временные файлы для классификации принципов
NEW_PRINCIPLES="${TMP_DIR}/new_principles.txt"
EXISTING_PRINCIPLES="${TMP_DIR}/existing_principles.txt"
> "${NEW_PRINCIPLES}"
> "${EXISTING_PRINCIPLES}"

# Обходим каждый сформулированный принцип
while IFS= read -r principle_line; do
    # Извлекаем саму фразу принципа из строки типа:
    # "Принцип (из поля Что сработало, 5 совпадений): Метод, доказавший свою эффективность..."
    if [[ "${principle_line}" =~ Принцип\ \(из\ поле\ [^,]+,\ [0-9]+\\ совпадений\):\ (.+) ]]; then
        principle_text="${BASH_REMATCH[1]}"
        
        # Убираем ведущие и尾随 пробелы
        principle_text=$(echo "${principle_text}" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
        
        if [ -z "${principle_text}" ]; then
            continue
        fi
        
        # Проверяем, существует ли уже примерно такой же принцип в библиотеке
        # Упрощённая проверка: ищем подстроку принципа в файле принципов
        # В будущем заменить на семантическое сравнение через эмбеддинги или внешний API
        if grep -iq "${principle_text}" "${PRINCIPLES_LIB}" 2>/dev/null; then
            # Принцип, кажется, уже существует
            echo "Принцип (возможно существует): ${principle_text}" >> "${EXISTING_PRINCIPLES}"
            log "  Принцип, кажется, уже существует в библиотеке: ${principle_text}"
        else
            # Принцип кажется новым
            echo "Новый принцип: ${principle_text}" >> "${NEW_PRINCIPLES}"
            log "  Новый princípio Candidate: ${principle_text}"
        fi
        
    else
        log "Предупреждение: не удалось распарсить строку принципа: ${principle_line}"
    fi
done < "${TMP_DIR}/all_principles_to_check.md"

# Подсчитаем количества
NEW_COUNT=$(wc -l < "${NEW_PRINCIPLES}" 2>/dev/null || echo 0)
EXISTING_COUNT=$(wc -l < "${EXISTING_PRINCIPLES}" 2>/dev/null || echo 0)

log "Найдено новых принципов: ${NEW_COUNT}"
log "Найдено потенциально существующих принципов: ${EXISTING_COUNT}"

# Если нет ни новых, ни существующих принципов для рассмотрения
if [ "${NEW_COUNT}" -eq 0 ] && [ "${EXISTING_COUNT}" -eq 0 ]; then
    log "ОШИБКА: Не найдено принципов для рассмотрения после проверки дублирования."
    exit 1
fi

log "Проверка принципов на дублирование завершена."

# Вывод принципов на экран для пользовательской валидации (человек-в-петле)
log "=== ПОЛЬЗОВАТЕЛЬСКАЯ ВАЛИДАЦИЯ ПРИНЦИПОВ ==="
log "Пожалуйста, просмотрите следующие сформулированные принципы и решите,"
log "какие из них достойны быть добавлены в навыки как проверенные знания."
log ""

# Счётчики для отчёта
VALIDATED_NEW=0
VALIDATED_EXISTING_UPDATED=0
REJECTED=0

# Временной файл для принципов, подтверждённых как новые
PRINCIPLES_TO_ADD="${TMP_DIR}/principles_to_add.txt"
> "${PRINCIPLES_TO_ADD}"

# Временной файл для принципов, отмеченных как требующих обновление существующих навыков
PRINCIPLES_TO_UPDATE_EXISTING="${TMP_DIR}/principles_to_update_existing.txt"
> "${PRINCIPLES_TO_UPDATE_EXISTING}"

# Функция для запроса подтверждения у пользователя
get_user_decision() {
    local principle_text="$1"
    local principle_type="$2"  # "new" или "existing"
    
    while true; do
        if [ "${principle_type}" = "new" ]; then
            echo -n "Добавить этот принцип как новый проверенный знания? (y/n/u): "
        else
            echo -n "Обновить существующий навык на основе этого принципа? (y/n/u): "
        fi
        read -r choice
        choice=$(echo "${choice}" | tr '[:upper:]' '[:lower:]')
        
        case "${choice}" in
            y|yes)
                echo "y"
                return 0
                ;;
            n|no)
                echo "n"
                return 0
                ;;
            u|update)
                echo "u"
                return 0
                ;;
            *)
                echo "Пожалуйста, введите y (да), n (нет) или u (обновить)."
                ;;
        esac
    done
}

# Обрабатываем новые принципы
if [ "${NEW_COUNT}" -gt 0 ]; then
    log "--- НОВЫЕ ПРИНЦИПЫ ---"
    echo "Новые принципы (не найдены в библиотеке principles_lib.md):"
    echo ""
    
    principle_num=1
    while IFS= read -r principle_line; do
        if [[ "${principle_line}" =~ Новый\ принцип:\ (.+) ]]; then
            principle_text="${BASH_REMATCH[1]}"
            
            echo ""
            echo "${principle_num}. Принцип: ${principle_text}"
            echo ""
            
            decision=$(get_user_decision "${principle_text}" "new")
            
            if [ "${decision}" = "y" ]; then
                echo "${principle_text}" >> "${PRINCIPLES_TO_ADD}"
                VALIDATED_NEW=$((VALIDATED_NEW + 1))
                log "  ✅ Принцип подтверждён как новый: ${principle_text}"
            elif [ "${decision}" = "u" ]; then
                echo "${principle_text}" >> "${PRINCIPLES_TO_UPDATE_EXISTING}"
                VALIDATED_EXISTING_UPDATED=$((VALIDATED_EXISTING_UPDATED + 1))
                log "  🔄 Принцип отмечен для обновления существующих навыков: ${principle_text}"
            else
                REJECTED=$((REJECTED + 1))
                log "  ❌ Принцип отклонён: ${principle_text}"
            fi
            
            principle_num=$((principle_num + 1))
        fi
    done < "${NEW_PRINCIPLES}"
fi

# Обрабатываем потенциально существующие принципы
if [ "${EXISTING_COUNT}" -gt 0 ]; then
    log "--- ПОТЕНЦИАЛЬНО СУЩЕСТВУЮЩИЕ ПРИНЦИПЫ ---"
    echo "Принципы, которые, кажется, уже существуют в библиотеке:"
    echo ""
    
    principle_num=1
    while IFS= read -r principle_line; do
        if [[ "${principle_line}" =~ Принцип\ \(возможно\ существует\):\ (.+) ]]; then
            principle_text="${BASH_REMATCH[1]}"
            
            echo ""
            echo "${principle_num}. Принцип: ${principle_text}"
            echo ""
            
            decision=$(get_user_decision "${principle_text}" "existing")
            
            if [ "${decision}" = "y" ]; then
                # Пользователь говорит: да, добавить как новый — несмотря на то, что мы думали, что он существует
                echo "${principle_text}" >> "${PRINCIPLES_TO_ADD}"
                VALIDATED_NEW=$((VALIDATED_NEW + 1))
                log "  ✅ Принцип подтверждён как новый (пользователь переопределил): ${principle_text}"
            elif [ "${decision}" = "u" ]; then
                echo "${principle_text}" >> "${PRINCIPLES_TO_UPDATE_EXISTING}"
                VALIDATED_EXISTING_UPDATED=$((VALIDATED_EXISTING_UPDATED + 1))
                log "  🔄 Принцип отмечен для обновления существующих навыков: ${principle_text}"
            else
                REJECTED=$((REJECTED + 1))
                log "  ❌ Принцип отклонён: ${principle_text}"
            fi
            
            principle_num=$((principle_num + 1))
        fi
    done < "${EXISTING_PRINCIPLES}"
fi

# Итоговый подсчёт
TOTAL_PROCESSED=$((NEW_COUNT + EXISTING_COUNT))
log "=== ИТОГИ ВАЛИДАЦИИ ==="
log "Всего принципов представлено на валидацию: ${TOTAL_PROCESSED}"
log "Подтверждено как новые для добавления: ${VALIDATED_NEW}"
log "Отмечено для обновления существующих навыков: ${VALIDATED_EXISTING_UPDATED}"
log "Отклонено: ${REJECTED}"

# Если нет принципов для добавления — предупреждаем, но продолжаем
if [ "${VALIDATED_NEW}" -eq 0 ] && [ "${VALIDATED_EXISTING_UPDATED}" -eq 0 ]; then
    log "Предупреждение: не подтверждено ни одного принципа для добавления или обновления."
    log "Кристаллизация завершится без изменений в навыках."
else
    log "Будет выполнено обновление навыков на основе подтверждённых принципов."
fi

log "Пользовательская валидация завершена."

# Обновление навыков: запись подтверждённых принципов в skills/*/references/
log "=== ОБНОВЛЕНИЕ НАВЫКОВ: ЗАПИСЬ ПРИНЦИПОВ В SKILLS/*/REFERENCES/ ==="

# Если нет принципов для добавления — пропускаем
if [ ! -s "${PRINCIPLES_TO_ADD}" ]; then
    log "Предупреждение: нет принципов, подтверждённых как новые для добавления в навыки."
else
    log "Найдено принципов для добавления в навыки: $(wc -l < "${PRINCIPLES_TO_ADD}")"
    
    # Обходим каждый принцип, подтверждённый пользователем
    while IFS= read -r principle_text; do
        if [ -z "${principle_text}" ]; then
            continue
        fi
        
        log "Обработ принципа для добавления: ${principle_text}"
        
        # Определяем целевой skill на основе ключевых слов в принципе
        # Это упрощённый роутер — в будущем можно сделать более умным
        TARGET_SKILL_DIR=""
        
        principle_lower=$(echo "${principle_text}" | tr '[:upper:]' '[:lower:]')
        
        # Проверяем наличие явных упоминаний доменов
        if echo "${principle_lower}" | grep -q "agronomy\|сельское\|земледелие\|урожай\|растени\|почва\|удобрени\|полив"; then
            TARGET_SKILL_DIR="agronomy_advisor"
        elif echo "${principle_lower}" | grep -q "iot\|датчик\|sensor\|эко\|мониторинг\|полив\|вода\|влажность\|тemperatur\|ec\|ph"; then
            TARGET_SKILL_DIR="iot_monitor"
        elif echo "${principle_lower}" | grep -q "вино\|виноград\|виноградарство\|виноградни\|фенофаз\|болезнь\|химзащита"; then
            TARGET_SKILL_DIR="viticulture"
        elif echo "${principle_lower}" | grep -q "ии\|ai\|искусственный\|интеллект\|машинное\|обучение\|llm\|агент"; then
            TARGET_SKILL_DIR="ai_tools"
        elif echo "${principle_lower}" | grep -q "отчёт\|report\|документация\|документ\|доклад\|сводка"; then
            TARGET_SKILL_DIR="report_generator"
        else
            # Если домен не определён — используем первый доступный skill с references/
            log "  Домен не определён по ключевым словам — поиск первого доступного навыка с references/..."
            for skill_dir in "${SKILLS_DIR}"/*/; do
                if [ -d "${skill_dir}" ] && [ -d "${skill_dir}references/" ]; then
                    TARGET_SKILL_DIR=$(basename "${skill_dir}")
                    log "  Выбран навык по умолчанию: ${TARGET_SKILL_DIR}"
                    break
                fi
            done
        fi
        
        # Если всё ещё не нашли skill — используем общий fallback
        if [ -z "${TARGET_SKILL_DIR}" ]; then
            TARGET_SKILL_DIR="agronomy_advisor"  # или любой другой
            log "  Не удалось определить навык — использован fallback: ${TARGET_SKILL_DIR}"
        fi
        
        # Формируем путь к директории references целевого навыка
        TARGET_REFERENCES_DIR="${SKILLS_DIR}/${TARGET_SKILL_DIR}/references/"
        
        # Убедимся, что директория существует
        if [ ! -d "${TARGET_REFERENCES_DIR}" ]; then
            log "  ОШИБКА: Директория references не существует: ${TARGET_REFERENCES_DIR}"
            log "  Пропускаем принцип: ${principle_text}"
            continue
        fi
        
        # Формируем имя файла для принципа на основе содержания (упрощённый хеш)
        # В будущем можно использовать заголовок принципа или UUID
        principle_hash=$(echo "${principle_text}" | md5sum | cut -c1-8)
        principle_file="${TARGET_REFERENCES_DIR}/principle_${principle_hash}.md"
        
        # Проверяем, не существует ли уже примерно такой же принцип в этом каталоге
        # Упрощённая проверка по подстроке
        if grep -iq "${principle_text}" "${TARGET_REFERENCES_DIR}"/*.md 2>/dev/null; then
            log "  Предупреждение: похожий принцип уже существует в ${TARGET_REFERENCES_DIR} — пропускаем, чтобы избежать дублирования"
            continue
        fi
        
        # Формируем содержимое файла принципа
        {
            echo "# Принцип, кристаллизованный из опыта"
            echo ""
            echo "**Принцип**: ${principle_text}"
            echo ""
            echo "**Источник**: кристаллизация опыта через навык crystallizer"
            echo "**Дата кристаллизации**: $(date '+%Y-%m-%d')"
            echo "**Метрики (EvolveR)**: applied_count=0, success_rate=0.0 (будет обновляться при применении)"
            echo "**Статус**: active"
            echo ""
            echo "> Этот принцип был извлечён из накопленного опыта через процесс"
            echo "> Knowledge Crystallization Cycle (NFD) и проверен пользователем."
            echo "> Он готов к применению в будущей работе и последующей оценке эффективности."
        } > "${principle_file}"
        
        log "  ✅ Принцип записан в навык: ${TARGET_SKILL_DIR}"
        log "     Файл: ${principle_file}"
        
    done < "${PRINCIPLES_TO_ADD}"
    
    log "Обновление навыков через запись новых принципов завершено."
fi

# Обработка принципов, отмеченных для обновления существующих навыков
# В этой версии мы просто логируем их — в будущем можно было бы
# увеличивать applied_count или переобучать навык
if [ -s "${PRINCIPLES_TO_UPDATE_EXISTING}" ]; then
    log "=== ОБНОВЛЕНИЕ СУЩЕСТВУЮЩИХ НАВЫКОВ ==="
    log "Найдено принципов, отмеченных для обновления существующих навыков: $(wc -l < "${PRINCIPLES_TO_UPDATE_EXISTING}")"
    
    while IFS= read -r principle_text; do
        if [ -z "${principle_text}" ]; then
            continue
        fi
        log "  Принцип для обновления существующих навыков: ${principle_text}"
        # В будущем здесь мог бы быть код для:
        # - Поиска существующих принципов в onвыках
        # - Обновления их метрик (applied_count++)
        # - Переобучения или корректировки навыка
        # Пока просто логируем — задача будущего этапа
    done < "${PRINCIPLES_TO_UPDATE_EXISTING}"
    
    log "Отмечено для обновления существующих навыков (жёсткая логика будет добавлена в будущих версиях)."
else
    log "Нет принципов, отмеченных для обновления существующих навыков."
fi

log "Обновление навыков завершено."

# Работа с библиотекой принципов (memory/principles_lib.md): отметка устаревших и обновление метрик
log "=== РАБОТА С БИБЛИОТЕКОЙ ПРИНЦИПОВ: ОБНОВЛЕНИЕ МЕТРИК И ОТМЕТКА УСТАРЕВШИХ ==="

# Если библиотека принципов пуста — просто отмечаем, что нет данных для анализа
if [ ! -s "${PRINCIPLES_LIB}" ]; then
    log "Предупреждение: библиотека принципов пуста — нет данных для обновления метрик или отметки устаревших."
else
    log "Найдена библиотека принципов: ${PRINCIPLES_LIB}"
    
    # Временной файл для обновлённой библиотеки
    PRINCIPLES_LIB_UPDATED="${TMP_DIR}/principles_lib_updated.md"
    > "${PRINCIPLES_LIB_UPDATED}"
    
    # Флаг, указывающий, был ли принцип подтверждён в текущем сеансе
    # Мы будем использовать список подтверждённых принципов для отметки
    
    # Создадим множество подтверждённых принципов (текст принципа)
    DECLARED_VALID_PRINCIPLES="${TMP_DIR}/declared_valid_principles.txt"
    > "${DECLARED_VALID_PRINCIPLES}"
    
    # Собираем все принципы, подтверждённые пользователем (как новые или как существующие для обновления)
    if [ -s "${PRINCIPLES_TO_ADD}" ]; then
        cat "${PRINCIPLES_TO_ADD}" >> "${DECLARED_VALID_PRINCIPLES}"
    fi
    if [ -s "${PRINCIPLES_TO_UPDATE_EXISTING}" ]; then
        cat "${PRINCIPLES_TO_UPDATE_EXISTING}" >> "${DECLARED_VALID_PRINCIPLES}"
    fi
    
    # Обходим каждый блок принципа в библиотеке principles_lib.md
    # Предполагаем формат:
    # ## Принцип: ...
    # **Домен**: ...
    # **Источник**: ...
    # **Метрики**: applied_count=X, success_rate=Y.Z, last_applied=DATE
    # **Статус**: active
    
    # Упрощённый парсер: читаем файл блоками, разделёнными пустыми строками или заголовками ##
    
    log "Начало обработки блоков принципов в библиотеке..."
    
    # Временные переменные для накопления текущего блока
    current_block=""
    in_block=0
    
    # Читаем файл построчно
    while IFS= read -r line || [ -n "${line}" ]; do
        # Проверяем, является ли строка началом нового блока принципа
        if [[ "${line}" =~ ^##\ Принцип:\ .+ ]]; then
            # Если у нас был накопленный блок — обрабатываем его
            if [ "${in_block}" -eq 1 ] && [ -n "${current_block}" ]; then
                # Извлекаем текст принципа из блока
                principle_from_block=""
                if [[ "${current_block}" =~ \*\*Принцип\*\*:[[:space:]]*(.+) ]]; then
                    principle_from_block="${BASH_REMATCH[1]}"
                    principle_from_block=$(echo "${principle_from_block}" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
                fi
                
                # Проверяем, был ли этот принцип подтверждён пользователем в текущем сеансе
                is_confirmed=0
                if [ -n "${principle_from_block}" ]; then
                    # Ищем точное совпадение в списке подтверждённых принципов
                    # Упрощённо: ищем подстроку (в будущем можно сделать точнее)
                    if grep -q "${principle_from_block}" "${DECLARED_VALID_PRINCIPLES}" 2>/dev/null; then
                        is_confirmed=1
                    fi
                fi
                
                # Обрабатываем блок в зависимости от того, подтверждён ли он
                if [ "${is_confirmed}" -eq 1 ] || [ "${in_block}" -eq 0 ]; then
                    # Если принцип подтверждён или это первый блок (заголовок) — просто пропускаем через
                    echo "${current_block}" >> "${PRINCIPLES_LIB_UPDATED}"
                else
                    # Принцип не подтверждён в этом сеансе — помечаем как требующий пересмотра
                    # Мы добавляем комментарий или меняем статус
                    # Упрощённо: заменяем строку **Статус**: active на **Статус**: under_review
                    modified_block=$(echo "${current_block}" | sed 's/\*\*Статус\*\*: active/\*\*Статус\*\*: under_review/')
                    echo "${modified_block}" >> "${PRINCIPLES_LIB_UPDATED}"
                    log "  Принцип помечен как under_review (не подтверждён в этом сеансе): ${principle_from_block}"
                fi
                
                # Сбрасываем блок для следующего
                current_block=""
                in_block=0
            fi
            
            # Начинаем новый блок
            current_block="${line}"
            in_block=1
        elif [ "${in_block}" -eq 1 ]; then
            # Добавляем строку к текущему блоку
            current_block="${current_block}${line}"
        else
            # Строка вне какого-либо блока — просто пропускаем через (заголовки, пустые строки между блоками)
            echo "${line}" >> "${PRINCIPLES_LIB_UPDATED}"
        fi
    done < "${PRINCIPLES_LIB}"
    
    # Обрабатываем последний блок, если файл не заканчивается на пустую строку
    if [ "${in_block}" -eq 1 ] && [ -n "${current_block}" ]; then
        # Извлекаем текст принципа из блока
        principle_from_block=""
        if [[ "${current_block}" =~ \*\*Принцип\*\*:[[:space:]]*(.+) ]]; then
            principle_from_block="${BASH_REMATCH[1]}"
            principle_from_block=$(echo "${principle_from_block}" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')
        fi
        
        # Проверяем, был ли этот принцип подтверждён пользователем в текущем сеансе
        is_confirmed=0
        if [ -n "${principle_from_block}" ]; then
            if grep -q "${principle_from_block}" "${DECLARED_VALID_PRINCIPLES}" 2>/dev/null; then
                is_confirmed=1
            fi
        fi
        
        # Обрабатываем блок
        if [ "${is_confirmed}" -eq 1 ]; then
            echo "${current_block}" >> "${PRINCIPLES_LIB_UPDATED}"
        else
            modified_block=$(echo "${current_block}" | sed 's/\*\*Статус\*\*: active/\*\*Статус\*\*: under_review/')
            echo "${modified_block}" >> "${PRINCIPLES_LIB_UPDATED}"
            log "  Принцип помечен как under_review (не подтверждён в этом сеансе): ${principle_from_block}"
        fi
    fi
    
    # Заменяем исходный файл библиотеки на обновлённый
    mv "${PRINCIPLES_LIB_UPDATED}" "${PRINCIPLES_LIB}"
    log "Библиотека принципов обновлена: ${PRINCIPLES_LIB}"
    
    # Подсчитаем количество принципов, помеченных как under_review
    UNDER_REVIEW_COUNT=$(grep -c '\*\*Статус\*\*: under_review' "${PRINCIPLES_LIB}" 2>/dev/null || echo 0)
    log "Принципов помеченных как under_review (требуют пересмотра): ${UNDER_REVIEW_COUNT}"
    
fi

log "Работа с библиотекой принципов завершена."

# Обновление MEMORY.md сводкой новых кристаллизованных знаний
log "=== ОБНОВЛЕНИЕ MEMORY.MD: СВОДКА НОВЫХ КРИСТАЛЛИЗОВАННЫХ ЗНАНИЙ ==="

# Формируем строку сводки
SUMMARY_LINE="* $(date '+%d.%m.%Y'): Урок из кристаллизации опыта"
SUMMARY_LINE="${SUMMARY_LINE} — сформулировано ${TOTAL_PRINCIPLE_COUNT} потенциальных принципов"
SUMMARY_LINE="${SUMMARY_LINE}, подтверждено как новые для добавления: ${VALIDATED_NEW}"
if [ "${VALIDATED_EXISTING_UPDATED}" -gt 0 ]; then
    SUMMARY_LINE="${SUMMARY_LINE}, отмечено для обновления существующих навыков: ${VALIDATED_EXISTING_UPDATED}"
fi
if [ "${REJECTED}" -gt 0 ]; then
    SUMMARY_LINE="${SUMMARY_LINE}, отклонено: ${REJECTED}"
fi
if [ "${UNDER_REVIEW_COUNT:-0}" -gt 0 ]; then
    SUMMARY_LINE="${SUMMARY_LINE}, принципов помечено как under_review: ${UNDER_REVIEW_COUNT}"
fi

# Добавляем сводку в MEMORY.md
echo "${SUMMARY_LINE}" >> "${MEMORY_SUMMARY}"

log "Сводка добавлена в MEMORY.md: ${SUMMARY_LINE}"
log "Обновление MEMORY.md завершено."

# Генерация отчёта о кристаллизации в plans/
log "=== ГЕНЕРАЦИЯ ОТЧЁТА О КРИСТАЛЛИЗАЦИИ В PLANS/ ==="

# Формируем имя файла отчёта
REPORT_FILE="${PLANS_DIR}/crystallization_report_${TIMESTAMP_FILE}.md"

# Формируем содержимое отчёта
{
    echo "# Отчёт о кристаллизации знаний"
    echo ""
    echo "**Навык**: crystallizer (NFD Knowledge Crystallization Cycle + EvolveR)"
    echo "**Дата и время запуска**: ${START_TIME}"
    echo "**Дата и время завершения**: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo "## 📊 Метрики обработки"
    echo ""
    echo "- **Обработано записей опыта**: ${RECORD_COUNT}"
    echo "- **Сформулировано потенциальных принципов**: ${TOTAL_PRINCIPLE_COUNT}"
    echo ""
    echo "## 👥 Результаты пользовательской валидации"
    echo ""
    echo "- **Подтверждено как новые для добавления в навыки**: ${VALIDATED_NEW}"
    echo "- **Отмечено для обновления существующих навыков**: ${VALIDATED_EXISTING_UPDATED}"
    echo "- **Отклонено пользователем**: ${REJECTED}"
    echo ""
    echo "## 📜 Подтвержденные принципы для добавления в навыки"
    echo ""
    if [ "${VALIDATED_NEW}" -gt 0 ]; then
        echo "Список принципов, подтверждённых пользователем как новые и достойные добавления в skill references/:"
        echo ""
        while IFS= read -r principle; do
            if [ -n "${principle}" ]; then
                echo "- ${principle}"
            fi
        done < "${PRINCIPLES_TO_ADD}"
        echo ""
    else
        echo "*Нет принципов, подтвержденных как новые для добавления.*"
        echo ""
    fi
    
    echo "## 🔄 Принципы, отмеченные для обновления существующих навыков"
    echo ""
    if [ "${VALIDATED_EXISTING_UPDATED}" -gt 0 ]; then
        echo "Список принципов, отмеченных пользователем как достойные для использования в обновлении существующих навыков:"
        echo ""
        while IFS= read -r principle; do
            if [ -n "${principle}" ]; then
                echo "- ${principle}"
            fi
        done < "${PRINCIPLES_TO_UPDATE_EXISTING}"
        echo ""
    else
        echo "*Нет принципов, отмеченных для обновления существующих навыков.*"
        echo ""
    fi
    
    echo "## 🧠 Работа с библиотекой принципов (memory/principles_lib.md)"
    echo ""
    echo "- **Библиотека принципов использована для проверки дублирования**: ${PRINCIPLES_LIB}"
    echo "- **Принципов помечено как under_review (требуют пересмотра)**: ${UNDER_REVIEW_COUNT:-0}"
    echo ""
    echo "> Принципы помечены как under_review, если они были обнаружены как существующие в библиотеке"
    echo "> но не были подтверждены пользователем в текущем сеансе кристаллизации."
    echo "> Это упрощённая мера — в будущем заменить на реальную метрику эффективности (success_rate < 0.4 и applied_count > 5)."
    echo ""
    
    echo "## 🛠️ Обновление навыков (skills/*/references/)"
    echo ""
    if [ "${VALIDATED_NEW}" -gt 0 ]; then
        echo "Навыки, в которые были записаны новые подтверждённые принципы:"
        echo ""
        # Собираем информацию о том, в какие навыки записаны принципы
        # Для простоты мы просто перечислим файлы, созданные в references/
        # В будущем можно сделать более детальный отчёт с привязкой принципа к навыку
        if [ -d "${SKILLS_DIR}" ]; then
            echo "Обновленные директории references/:"
            find "${SKILLS_DIR}" -name "references" -type d | while read -r ref_dir; do
                # Покажем, если в директории есть недавние файлы (изменены в последние час)
                if [ -n "$(find "${ref_dir}" -name "*.md" -newer "${TMP_DIR}" 2>/dev/null)" ]; then
                    skill_name=$(basename "$(dirname "${ref_dir}")")
                    echo "- ${skill_name}: ${ref_dir}"
                fi
            done
        fi
        echo ""
    else
        echo "*Навыки не были обновлены новыми принципами в этом сеансе.*"
        echo ""
    fi
    
    echo "## 📝 Дальнейшие шаги и рекомендации"
    echo ""
    echo "1. **Проверьте обновленные навыки**: пересмотрите файлы в skills/*/references/ на предмет новых принципов"
    echo "2. **Применяйте новые принципы в работе**: используйте их при принятии решений и решении задач"
    echo "3. **Отслеживайте эффективность**: в будущих версиях навыка crystallizer будут отслеживаться метрики"
    echo "   (applied_count, success_rate) для каждого принципа в memory/principles_lib.md"
    echo "4. **Планируйте следующую кристаллизацию**:"
    echo "   - По расписанию: каждые 2 недели"
    echo "   - По порогу: при накоплении >5 записей с тегом [ERROR] одного типа"
    echo "   - По событию: после завершения сезонного агроцикла, крупного IoT-инцидента, нового проекта"
    echo ""
    echo "## 📎 Приложение: технические детали"
    echo ""
    echo "- **Скрипт**: ${0}"
    echo "- **Рабочая директория**: ${WORKSPACE_ROOT}"
    echo "- **Папка memory/**: ${MEMORY_DIR}"
    echo "- **Папка plans/**: ${PLANS_DIR}"
    echo "- **Папка skills/**: ${SKILLS_DIR}"
    echo "- **Временная директория обработки**: ${TMP_DIR} (очищена после завершения)"
    echo ""
    echo "> Отчёт сгенерирован навыком crystallizer как часть процесса Knowledge Crystallization Cycle (NFD)"
    echo "> и EvolveR метрики эффективности принципов."
    echo ""
} > "${REPORT_FILE}"

log "Отчёт о кристаллизации записан в: ${REPORT_FILE}"
log "Генерация отчёта завершена."

# Завершающее сообщение
log "=== ВЫПОЛНЕНИЕ НАВЫКА CRYSTALLIZER ЗАВЕРШЕНО ==="
log "Скрипт выполнен успешно."
log "Отчёт доступен в: ${REPORT_FILE}"
log "Библиотека принципов обновлена: ${PRINCIPLES_LIB}"
log "Навыки потенциально обновлены: проверьте skills/*/references/"
log "MEMORY.md обновлён сводкой знаний: ${MEMORY_SUMMARY}"
log ""
log "Следующий шаг: применять новые принципы в работе и следить за их эффективностью."
log "Следующая кристаллизация рекомендуется через 2 недели или по достижении пороговых условий."

# Возврат кода успеха
exit 0
