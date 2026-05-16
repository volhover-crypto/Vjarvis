#!/bin/bash

# skills/reflexion_loop/scripts/reflexion_loop.sh
# Скрипт навыка reflexion_loop: генерация структурированной записи рефлексии
# Часть навыка OpenClaw: skills/reflexion_loop/
# Реализует NFD Experiential Layer + EvolveR 원칙 извлечения и использования

set -euo pipefail

# Конфигурация
MEMORY_DIR="/root/.openclaw/workspace/memory"
PRINCIPLES_LIB="${MEMORY_DIR}/principles_lib.md"
TODAY=$(date '+%Y-%m-%d')
DAILY_LOG="${MEMORY_DIR}/${TODAY}.md"
TIMESTAMP=$(date '+%H:%M')

# Убедимся, что директория и файлы существуют
mkdir -p "${MEMORY_DIR}"
touch "${DAILY_LOG}"
touch "${PRINCIPLES_LIB}"

# Заголовок дневного лога, если файл пустой
if [ ! -s "${DAILY_LOG}" ]; then
    cat > "${DAILY_LOG}" <<EOF
# ${DAILY_LOG} — Дневной лог (append-only, NFD Experiential Layer)

> Структурированные записи опыта за день.  
> Каждая запись содержит: тип, домен, задачу, что сработало/не сработало, чего не хватало, принцип для будущего, уровень уверенности.  
> Использует теги: [OPERATIONAL_RECORD], [INSIGHT], [ERROR], [PATTERN], [DECISION], [CASE]  
> Формат основан на Nurture-First Development (NFD) — Experiential Layer.

EOF
fi

# Функция для добавления записи принципа в библиотеку (упрощённая версия)
add_principle_to_lib() {
    local principle="$1"
    local domain="$2"
    local timestamp="$3"
    
    # Проверяем, не существует ли уже примерно такой же принцип (простая проверка по подстроке)
    # В будущем можно заменить на семантическое сравнение через внешний API или эмбеддинги
    if grep -q ".*${principle}.*" "${PRINCIPLES_LIB}" 2>/dev/null; then
        # Принцип, кажется, уже существует — в полной версии здесь бы обновлялись метрики
        # Пока просто отмечаем, что принцип известен
        echo "Принцип, кажется, уже известен: ${principle}" >&2
        # Здесь можно было бы увеличить applied_count и обновить last_applied
        # Но для простоты оставляем как есть — эволюция принципов — задача будущего этапа
        return 1
    else
        # Добавляем новый принцип в библиотеку
        {
            echo ""
            echo "## Принцип: ${principle}"
            echo "**Домен**: ${domain}"
            echo "**Источник**: рефлексия от ${timestamp} ${TODAY}"
            echo "**Метрики**: applied_count=1, success_rate=1.0, last_applied=${TODAY}"
            echo "**Статус**: active"
        } >> "${PRINCIPLES_LIB}"
        echo "Новый принцип добавлен в библиотеку: ${principle}"
        return 0
    fi
}

# Основная функция: запрос рефлексии у пользователя и запись в лог
conduct_reflection() {
    echo "=== Навык reflexion_loop: структурированная рефлексия ==="
    echo "Этот навык помогает превратить неявный опыт в явное знание."
    echo "Пожалуйста, ответьте на следующие вопросы:"
    echo ""

    # Запрос типа записи
    echo "Выберите тип записи:"
    echo "  [DECISION] — принятое решение с обоснованием"
    echo "  [INSIGHT]  — новое понимание или аналогия"
    echo "  [ERROR]    — ошибка или неудачное действие"
    echo "  [PATTERN]  — наблюдаемый повторяющийся паттерн"
    echo "  [CASE]     — кейс: реальная ситуация и её разбор"
    echo -n "Введите тип (DECISION/INSIGHT/ERROR/PATTERN/CASE): "
    read -r REFLECTION_TYPE
    REFLECTION_TYPE=$(echo "${REFLECTION_TYPE}" | tr '[:lower:]' '[:upper:]')

    # Валидация типа
    if [[ ! "${REFLECTION_TYPE}" =~ ^(DECISION|INSIGHT|ERROR|PATTERN|CASE)$ ]]; then
        echo "Ошибка: неверный тип. Используется значение по умолчанию: INSIGHT"
        REFLECTION_TYPE="INSIGHT"
    fi

    # Запрос домена
    echo -n "Введите домен [agronomy/iot/ai_tools/viticulture/general]: "
    read -r REFLECTION_DOMAIN
    REFLECTION_DOMAIN=$(echo "${REFLECTION_DOMAIN}" | tr '[:lower:]' '[:lower:]')

    # Валидация домена (простая)
    if [[ ! "${REFLECTION_DOMAIN}" =~ ^(agronomy|iot|ai_tools|viticulture|general)$ ]]; then
        echo "Предупреждение: нестандартный домен. Используется как есть."
    fi

    # Запрос задачи
    echo -n "Кратко опишите задачу, над которой вы работали: "
    read -r REFLECTION_TASK

    # Запрос: что сработало
    echo -n "Что сработало в этом процессе?: "
    read -r REFLECTION_WENT_WELL

    # Запрос: что не сработало
    echo -n "Что не сработало или вызвало трудности?: "
    read -r REFLECTION_WENT_WRONG

    # Запрос: чего не хватало
    echo -n "Чего не хватало (контекст, данные, знание, инструменты)?: "
    read -r REFLECTION_MISSING

    # Запрос: принцип для будущего
    echo -n "Сформулируйте один принцип для будущего на основе этого опыта: "
    read -r REFLECTION_PRINCIPLE

    # Запрос: уровень уверенности
    # Запрос: уровень уверенности
    echo -n "Оцените уровень уверенности в этом выводе [Высокий/Средний/Низкий]: "
    read -r REFLECTION_CONFIDENCE

    # Приведём к нижнему регистру и уберём ведущие/конечные пробелы
    REFLECTION_CONFIDENCE=$(echo "${REFLECTION_CONFIDENCE}" | tr '[:upper:]' '[:lower:]' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')

    # Маппинг уверенности
    case "${REFLECTION_CONFIDENCE}" in
        высокий|высокая|high)
            CONFIDENCE_TEXT="Высокий"
            ;;
        средний|средняя|medium|medium)
            CONFIDENCE_TEXT="Средний"
            ;;
        низкий|низкая|low)
            CONFIDENCE_TEXT="Низкий"
            ;;
        *)
            echo "Предупреждение: неверный формат уверенности. Используется Средний."
            CONFIDENCE_TEXT="Средний"
            ;;
    esac

    case "${REFLECTION_CONFIDENCE}" in

        высокий|высокая|high)

            CONFIDENCE_TEXT="Высокий"

            ;;

        средний|средняя|medium|medium)

            CONFIDENCE_TEXT="Средний"

            ;;

        низкий|низкая|low)

            CONFIDENCE_TEXT="Низкий"

            ;;

        *)

            echo "Предупреждение: неверный формат уверенности. Используется Средний."

            CONFIDENCE_TEXT="Средний"

            ;;

    esac


        *) CONFIDENCE_TEXT="Средний" ;; # fallback
    esac

    # Формируем запись рефлексии
    {
        echo ""
        echo "## [REFLECTION] ${TIMESTAMP} — ${REFLECTION_TASK}"
        echo ""
        echo "**Тип**: [${REFLECTION_TYPE}]"
        echo "**Домен**: ${REFLECTION_DOMAIN}"
        echo "**Задача**: ${REFLECTION_TASK}"
        echo ""
        echo "**Что сработало**: "
        echo "${REFLECTION_WENT_WELL}"
        echo ""
        echo "**Что не сработало**: "
        echo "${REFLECTION_WENT_WRONG}"
        echo ""
        echo "**Чего не хватало** (контекст, данные, знание): "
        echo "${REFLECTION_MISSING}"
        echo ""
        echo "**Принцип для будущего**: ${REFLECTION_PRINCIPLE}"
        echo ""
        echo "**Уровень уверенности в выводе**: ${CONFIDENCE_TEXT}"
        echo ""
    } >> "${DAILY_LOG}"

    echo ""
    echo "✅ Запись рефлексии добавлена в ${DAILY_LOG}"

    # Попытка добавить принцип в библиотеку (EvolveR-расширение)
    if [ -n "${REFLECTION_PRINCIPLE}" ]; then
        echo ""
        echo "🔄 Попытка добавить принцип в библиотеку EvolveR..."
        add_principle_to_lib "${REFLECTION_PRINCIPLE}" "${REFLECTION_DOMAIN}" "${TIMESTAMP}" || true
    fi

    echo ""
    echo "💡 Совет: для полной автоматизации принципов используйте семантическое сравнение"
    echo "   и обновление метрик (applied_count, success_rate) — задача будущего этапа."
    echo ""
    echo "Рефлексия завершена."
}

# Запуск основной функции
conduct_reflection