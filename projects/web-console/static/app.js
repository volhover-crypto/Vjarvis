/**
 * Jarvis Web Console v2.0 — Клиентская логика
 */

// ─── Состояние ─────────────────────────────────────────────────

let isLoading = false;
let statusInterval = null;
let csrfToken = "";

// ─── Login ─────────────────────────────────────────────────────

function initLogin() {
    const input = document.getElementById('password');
    if (input) input.focus();
}

async function doLogin(e) {
    e.preventDefault();
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');
    errorDiv.style.display = 'none';

    try {
        const resp = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `password=${encodeURIComponent(password)}`,
        });

        if (resp.ok) {
            const data = await resp.json();
            csrfToken = data.csrf_token || "";
            window.location.reload();
        } else if (resp.status === 429) {
            errorDiv.textContent = 'Слишком много попыток. Подождите 5 минут.';
            errorDiv.style.display = 'block';
        } else {
            const data = await resp.json().catch(() => null);
            errorDiv.textContent = data?.detail || 'Неверный пароль';
            errorDiv.style.display = 'block';
        }
    } catch (err) {
        errorDiv.textContent = 'Ошибка соединения с сервером';
        errorDiv.style.display = 'block';
    }
    return false;
}

async function doLogout() {
    try {
        await fetch('/api/logout', {
            method: 'POST',
            headers: { 'X-CSRF-Token': csrfToken },
        });
    } catch (e) { /* ignore */ }
    window.location.reload();
}

// ─── Chat ──────────────────────────────────────────────────────

function initChat(token) {
    csrfToken = token || "";
    loadHistory();
    checkStatus();
    statusInterval = setInterval(checkStatus, 15000);
    const input = document.getElementById('msg-input');
    if (input) input.focus();
}

async function loadHistory() {
    try {
        const resp = await fetch('/api/history');
        if (!resp.ok) {
            if (resp.status === 401) {
                window.location.reload();
                return;
            }
            throw new Error(`HTTP ${resp.status}`);
        }
        const data = await resp.json();
        const container = document.getElementById('chat-messages');
        const systemMsg = container.querySelector('.msg.system');
        container.innerHTML = '';
        if (systemMsg) container.appendChild(systemMsg);

        if (data.messages && data.messages.length > 0) {
            if (systemMsg) systemMsg.style.display = 'none';
            data.messages.forEach(msg => appendMessage(msg.role, msg.content, msg.ts));
        }
        scrollToBottom();
    } catch (e) {
        console.error('Failed to load history:', e);
        appendMessage('system', 'Ошибка загрузки истории');
    }
}

async function checkStatus() {
    try {
        const resp = await fetch('/api/health');
        const data = await resp.json();
        const dot = document.getElementById('status-dot');
        if (dot) {
            dot.className = 'status-dot ' + (data.openclaw === 'online' ? 'online' : 'offline');
            dot.title = data.openclaw === 'online' ? 'Онлайн' : 'Отключён';
        }
    } catch (e) {
        const dot = document.getElementById('status-dot');
        if (dot) { dot.className = 'status-dot offline'; dot.title = 'Сервер недоступен'; }
    }
}

async function sendMsg(e) {
    e.preventDefault();
    if (isLoading) return false;

    const input = document.getElementById('msg-input');
    const text = input.value.trim();
    if (!text) return false;

    input.value = '';
    autoResize(input);
    appendMessage('user', text);
    scrollToBottom();

    isLoading = true;
    showTyping();

    try {
        const resp = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': csrfToken,
            },
            body: JSON.stringify({ message: text }),
        });

        removeTyping();

        if (resp.ok) {
            const data = await resp.json();
            appendMessage('assistant', data.reply || '(пусто)');
        } else if (resp.status === 401) {
            appendMessage('system', 'Сессия истекла. Перезагрузка...');
            setTimeout(() => window.location.reload(), 1500);
            return false;
        } else if (resp.status === 403) {
            appendMessage('system', 'CSRF ошибка. Перезагрузка...');
            setTimeout(() => window.location.reload(), 1500);
            return false;
        } else if (resp.status === 429) {
            appendMessage('system', 'Слишком много запросов. Подождите.');
        } else {
            const data = await resp.json().catch(() => null);
            appendMessage('system', `Ошибка: ${data?.detail || resp.statusText}`);
        }
    } catch (e) {
        removeTyping();
        appendMessage('system', 'Ошибка соединения с сервером');
    }

    isLoading = false;
    scrollToBottom();
    input.focus();
    return false;
}

// ─── UI helpers ────────────────────────────────────────────────

function appendMessage(role, content, ts) {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.className = 'msg ' + role;

    const timeStr = ts ? formatTime(ts) : formatTime(new Date().toISOString());

    if (role === 'system') {
        div.innerHTML = `<div class="msg-bubble">${escapeHtml(content)}</div>`;
    } else {
        const label = role === 'user' ? 'Ты' : 'Jarvis';
        const formatted = formatContent(content);
        div.innerHTML = `
            <div class="msg-header">${escapeHtml(label)} · ${timeStr}</div>
            <div class="msg-bubble">${formatted}</div>
        `;
    }

    container.appendChild(div);
    scrollToBottom();
}

function showTyping() {
    const container = document.getElementById('chat-messages');
    const div = document.createElement('div');
    div.id = 'typing-indicator';
    div.className = 'msg assistant';
    div.innerHTML = `
        <div class="msg-header">Jarvis</div>
        <div class="msg-bubble"><span class="typing-dots"><span></span><span></span><span></span></span></div>
    `;
    container.appendChild(div);
    scrollToBottom();
}

function removeTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

function clearChat() {
    if (!confirm('Очистить историю чата?')) return;
    fetch('/api/history', {
        method: 'DELETE',
        headers: { 'X-CSRF-Token': csrfToken },
    }).then(() => {
        const container = document.getElementById('chat-messages');
        container.innerHTML = '<div class="msg system"><div class="msg-bubble">История очищена.</div></div>';
    }).catch(() => {
        appendMessage('system', 'Ошибка очистки истории');
    });
}

function scrollToBottom() {
    const el = document.getElementById('chat-messages');
    el.scrollTop = el.scrollHeight;
}

function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

function handleKey(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMsg(e);
    }
}

// ─── Text formatting ───────────────────────────────────────────

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatContent(text) {
    let html = escapeHtml(text);

    // Код блоки ```code```
    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');

    // Инлайн код `code`
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Жирный **text**
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

    // Курсив *text*
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Ссылки [text](url)
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');

    // Списки
    html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, function(match) {
        return '<ul>' + match + '</ul>';
    });

    // Переносы строк
    html = html.replace(/\n/g, '<br>');

    // Убираем лишние <br> перед блочными элементами
    html = html.replace(/<br>(<pre>|<ul>)/g, '$1');
    html = html.replace(/(<\/pre>|<\/ul>)<br>/g, '$1');

    return html;
}

function formatTime(isoString) {
    try {
        const d = new Date(isoString);
        return d.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });
    } catch (e) {
        return '';
    }
}
