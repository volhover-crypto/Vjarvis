#!/bin/bash
# quick-check skill - скрипт выполнения
# Быстрая проверка статуса системы и ключевых сервисов

# Цвета для вывода (опционально, если поддерживается терминал)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Функция для безопасного выполнения команды с таймаутом
safe_run() {
    local cmd="$1"
    local timeout_sec=${2:-5}
    local result
    result=$(timeout "$timeout_sec" bash -c "$cmd" 2>&1) || {
        echo -e "${RED}❌ Ошибка или таймаут${NC}"
        return 1
    }
    echo "$result"
}

# Функция для проверки интернет-подключения
check_internet() {
    echo -e "${YELLOW}Проверка интернет-подключения...${NC}"
    if safe_run "ping -c 1 -W 2 1.1.1.1" "5"; then
        # Извлекаем время отклика
        local ping_time
        ping_time=$(ping -c 1 -W 2 1.1.1.1 | grep 'time=' | awk -F'time=' '{print $2}' | awk '{print $1}')
        echo -e "${GREEN}✅ Интернет доступен (отклик: ${ping_time}мс)${NC}"
        return 0
    else
        echo -e "${RED}❌ Нет интернет-подключения${NC}"
        return 1
    fi
}

# Функция для проверки ключевых сервисов
check_services() {
    echo -e "${YELLOW}Проверка ключевых сервисов...${NC}"
    
    # Проверяем GBrain (PostgreSQL на порту 5432)
    if safe_run "nc -z localhost 5432" "3" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ GBrain: Доступен (PostgreSQL на 5432)$NC"
    elif pgrep -f "gbrain" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ GBrain: Процесс запущен${NC}"
    else
        echo -e "${YELLOW}⚠️ GBrain: Статус неизвестен (проверьте запуск)$NC"
    fi

    # Проверяем Vikunja (по умолчанию на порту 3456)
    if safe_run "nc -z localhost 3456" "3" >/devraint 2>&1; then
        echo -e "${GREEN}✅ Vikunja: Доступен (http://localhost:3456)$NC"
    else
        echo -e "${YELLOW}⚠️ Vikunja: Не отвечает на порту 3456$NC"
    fi

    # Проверяем Tailscale
    if safe_run "tailscale status" "5" | grep -q "Logged in"; then
        echo -e "${GREEN}✅ Tailscale: Активен (логин выполнен)$NC"
    else
        echo -e "${YELLOW}⚠️ Tailscale: Не авторизован или не запущен$NC"
    fi

    # Проверяем ProtonMail (доступность веб-интерфейса)
    if safe_run "curl -s --max-time 5 --head https://mail.protonmail.com/login" "5" | grep -q "200 OK"; then
        echo -e "${GREEN}✅ ProtonMail: Веб-интерфейс доступен$NC"
    else
        echo -e "${YELLOW}⚠️ ProtonMail: Проверьте соединение или статус$NC"
    fi
}

# Функция для получения использования ресурсов
get_resource_usage() {
    echo -e "${YELLOW}Получение данных об использовании ресурсов...${NC}"
    
    # CPU usage: извлекаем процент idle (поле $9) и вычитаем из 100
    local cpu_idle_raw cpu_idle cpu_usage_str
    cpu_idle_raw=$(top -bn1 | grep "Cpu(s)" | awk '{print $9}')  # Например: 81.8id,
    cpu_idle=$(echo "$cpu_idle_raw" | sed 's/id,//')            # Убираем id, → 81.8
    cpu_usage_str=$(awk "BEGIN {printf \"%.1f\", 100 - $cpu_idle}")
    
    # Memory usage
    local mem_total mem_used mem_percent_str
    mem_total=$(free | grep Mem | awk '{print $2}')
    mem_used=$(free | grep Mem | awk '{print $3}')
    mem_percent_str=$(awk "BEGIN {printf \"%.1f\", 100 * $mem_used / $mem_total}")
    
    # Disk usage
    local disk_used disk_size disk_percent
    disk_used=$(df / | tail -1 | awk '{print $3}')
    disk_size=$(df / | tail -1 | awk '{print $2}')
    disk_percent=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    
    # Вычисляем ГБ для RAM и диска через awk
    local mem_used_gb mem_total_gb disk_used_gb disk_size_gb
    mem_used_gb=$(awk "BEGIN {printf \"%.1f\", $mem_used / 1024 / 1024}")
    mem_total_gb=$(awk "BEGIN {printf \"%.1f\", $mem_total / 1024 / 1024}")
    disk_used_gb=$(awk "BEGIN {printf \"%.1f\", $disk_used / 1024 / 1024}")
    disk_size_gb=$(awk "BEGIN {printf \"%.1f\", $disk_size / 1024 / 1024}")
    
    # Выводим результат через echo — надёжно и просто
    echo "- CPU: ${cpu_usage_str}%"
    echo "- RAM: ${mem_used_gb} ГБ / ${mem_total_gb} ГБ (${mem_percent_str}%)"
    echo "- Диск: ${disk_used_gb} ГБ / ${disk_size_gb} ГБ (${disk_percent}%)"
}

# Основная функция выполнения навыка
main() {
    echo -e "${GREEN}🔍 Быстрая проверка системы и ключевых сервисов${NC}"
    echo ""
    
    # Время и дата
    echo -e "${GREEN}🕒 Текущее время и дата:${NC}"
    date '+%d.%m.%Y %H:%M:%S %Z'
    echo ""
    
    # Ресурсы
    echo -e "${GREEN}💻 Использование ресурсов:${NC}"
    get_resource_usage
    echo ""
    
    # Сеть
    echo -e "${GREEN}🌐 Статус сетевого подключения:${NC}"
    check_internet
    echo ""
    
    # Сервисы
    echo -e "${GREEN}🔌 Состояние ключевых сервисов:${NC}"
    check_services
    echo ""
    
    echo -e "${GREEN}✅ Проверка завершена.${NC}"
}

# Запуск основной функции
main "$@"