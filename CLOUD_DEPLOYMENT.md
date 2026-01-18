# Cloud Deployment Guide - Развертывание в облаке

Руководство по запуску Polymarket Price Monitor в облаке для непрерывной работы 24/7.

## 🌟 Лучшие варианты облачных платформ

### Сравнение платформ

| Платформа | Цена | Сложность | Рекомендуется |
|-----------|------|-----------|---------------|
| **Railway** | $5/мес | 🟢 Легко | ⭐⭐⭐⭐⭐ |
| **Render** | Free/$7/мес | 🟢 Легко | ⭐⭐⭐⭐⭐ |
| **Fly.io** | Free/$5/мес | 🟡 Средне | ⭐⭐⭐⭐ |
| **DigitalOcean** | $4/мес | 🟡 Средне | ⭐⭐⭐⭐ |
| **AWS EC2** | ~$3/мес | 🔴 Сложно | ⭐⭐⭐ |
| **Google Cloud** | Free/$5/мес | 🔴 Сложно | ⭐⭐⭐ |
| **Heroku** | $7/мес | 🟢 Легко | ⭐⭐⭐ |
| **VPS (Vultr/Hetzner)** | $3-5/мес | 🟡 Средне | ⭐⭐⭐⭐ |

---

## 🚀 Вариант 1: Railway (Рекомендуется)

**Почему Railway?**
- ✅ Очень простая настройка (5 минут)
- ✅ Автоматический деплой из GitHub
- ✅ Бесплатный план ($5 кредитов в месяц)
- ✅ Постоянное хранилище для логов
- ✅ Мониторинг и логи встроены

### Шаг 1: Подготовка проекта

Создайте файл `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python price_monitor_service.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Создайте файл `Procfile`:
```
worker: python price_monitor_service.py
```

### Шаг 2: Загрузка на GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/polymarket-logger.git
git push -u origin main
```

### Шаг 3: Деплой на Railway

1. Зайдите на [railway.app](https://railway.app)
2. Нажмите "New Project" → "Deploy from GitHub repo"
3. Выберите ваш репозиторий
4. Railway автоматически определит Python и запустит проект
5. Готово! Сервис работает 24/7

### Шаг 4: Настройка хранилища

Railway автоматически сохраняет файлы в директории проекта.

### Шаг 5: Просмотр логов

В Railway Dashboard → Ваш проект → Вкладка "Deployments" → View Logs

**Стоимость:** ~$5/месяц (хватает бесплатных кредитов)

---

## 🎨 Вариант 2: Render (Тоже отличный)

**Почему Render?**
- ✅ Есть бесплатный план
- ✅ Простая настройка
- ✅ Автоматический SSL
- ✅ Подключение к GitHub

### Шаг 1: Подготовка

Создайте `render.yaml`:
```yaml
services:
  - type: worker
    name: polymarket-monitor
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python price_monitor_service.py
    plan: free  # или starter ($7/мес)
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
```

### Шаг 2: Деплой

1. Зайдите на [render.com](https://render.com)
2. New → Background Worker
3. Подключите GitHub репозиторий
4. Render автоматически задеплоит

**Важно:** На бесплатном плане сервис "засыпает" после 15 минут неактивности. Используйте платный план ($7/мес) для 24/7 работы.

---

## ☁️ Вариант 3: DigitalOcean Droplet (Больше контроля)

**Почему DigitalOcean?**
- ✅ Полный контроль
- ✅ Дешево ($4/мес)
- ✅ Простой SSH доступ
- ✅ 200$ кредитов для новых пользователей

### Шаг 1: Создание Droplet

1. Зайдите на [digitalocean.com](https://digitalocean.com)
2. Create → Droplets
3. Выберите:
   - Ubuntu 22.04 LTS
   - Basic Plan - $4/месяц (512MB RAM)
   - Регион: ближайший к вам

### Шаг 2: Подключение по SSH

```bash
ssh root@your_droplet_ip
```

### Шаг 3: Установка зависимостей

```bash
# Обновление системы
apt update && apt upgrade -y

# Установка Python и pip
apt install python3 python3-pip git -y

# Установка screen (для фоновой работы)
apt install screen -y
```

### Шаг 4: Загрузка проекта

```bash
# Создание директории
mkdir /opt/polymarket-logger
cd /opt/polymarket-logger

# Клонирование из GitHub (если есть)
git clone https://github.com/your-username/polymarket-logger.git .

# ИЛИ загрузка через SFTP/scp
# scp -r C:\Poly\Price_logger/* root@your_droplet_ip:/opt/polymarket-logger/
```

### Шаг 5: Установка зависимостей

```bash
pip3 install -r requirements.txt
```

### Шаг 6: Настройка config.json

```bash
nano config.json
# Отредактируйте конфигурацию
# Ctrl+O для сохранения, Ctrl+X для выхода
```

### Шаг 7: Запуск в фоне

```bash
# Создание screen сессии
screen -S polymarket

# Запуск сервиса
python3 price_monitor_service.py

# Нажмите Ctrl+A затем D для отключения от сессии
```

### Шаг 8: Автозапуск через systemd

Создайте файл `/etc/systemd/system/polymarket-monitor.service`:

```ini
[Unit]
Description=Polymarket Price Monitor Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/polymarket-logger
ExecStart=/usr/bin/python3 /opt/polymarket-logger/price_monitor_service.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запустите службу:
```bash
systemctl daemon-reload
systemctl enable polymarket-monitor
systemctl start polymarket-monitor

# Проверка статуса
systemctl status polymarket-monitor

# Просмотр логов
journalctl -u polymarket-monitor -f
```

### Шаг 9: Скачивание логов

```bash
# С сервера на локальный компьютер
scp -r root@your_droplet_ip:/opt/polymarket-logger/logs ./logs_backup
```

**Стоимость:** $4/месяц

---

## 🚁 Вариант 4: Fly.io (Современный подход)

**Почему Fly.io?**
- ✅ Бесплатный план (достаточно для нашего случая)
- ✅ Глобальная CDN
- ✅ Автоматическое масштабирование

### Шаг 1: Установка CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Linux/Mac
curl -L https://fly.io/install.sh | sh
```

### Шаг 2: Логин

```bash
fly auth login
```

### Шаг 3: Инициализация проекта

```bash
cd C:\Poly\Price_logger
fly launch
```

Fly.io создаст файл `fly.toml`:
```toml
app = "polymarket-monitor"

[build]
  builder = "paketobuildpacks/builder:base"

[processes]
  worker = "python price_monitor_service.py"

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 256
```

### Шаг 4: Создание Volume для логов

```bash
fly volumes create logs_data --size 1
```

Обновите `fly.toml`:
```toml
[[mounts]]
  source = "logs_data"
  destination = "/app/logs"
```

### Шаг 5: Деплой

```bash
fly deploy
```

### Шаг 6: Просмотр логов

```bash
fly logs
```

### Шаг 7: SSH доступ

```bash
fly ssh console
```

**Стоимость:** Бесплатно (в пределах лимитов)

---

## 💰 Вариант 5: Oracle Cloud Free Tier (Полностью бесплатно!)

**Почему Oracle Cloud?**
- ✅ Навсегда бесплатный план
- ✅ 2 VM с 1GB RAM каждая
- ✅ 200GB storage
- ✅ Нет ограничений по времени

### Настройка

1. Зарегистрируйтесь на [oracle.com/cloud/free](https://www.oracle.com/cloud/free/)
2. Создайте VM Instance (Always Free eligible)
3. Выберите Ubuntu 22.04
4. Следуйте инструкциям как для DigitalOcean (Вариант 3)

**Стоимость:** $0 (навсегда бесплатно!)

---

## 📊 Сравнение по параметрам

### По простоте настройки:
1. **Railway** - 5 минут ⭐⭐⭐⭐⭐
2. **Render** - 10 минут ⭐⭐⭐⭐
3. **Fly.io** - 15 минут ⭐⭐⭐
4. **DigitalOcean** - 20 минут ⭐⭐⭐
5. **Oracle Cloud** - 30 минут ⭐⭐

### По цене (месяц):
1. **Oracle Cloud** - $0 ⭐⭐⭐⭐⭐
2. **Fly.io** - $0-3 ⭐⭐⭐⭐⭐
3. **DigitalOcean** - $4 ⭐⭐⭐⭐
4. **Railway** - $5 ⭐⭐⭐⭐
5. **Render** - $7 ⭐⭐⭐

### По надежности:
Все платформы надежны для данной задачи (99.9% uptime).

---

## 🔧 Общие настройки для всех платформ

### 1. Переменные окружения (опционально)

Можно хранить чувствительные данные в переменных окружения:

```python
# В начале price_monitor_service.py
import os

CONFIG_FILE = os.getenv('CONFIG_PATH', 'config.json')
```

### 2. Мониторинг работы

Добавьте простой health check endpoint (опционально):

```python
# health_check.py
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')

    def log_message(self, format, *args):
        pass  # Отключаем логи

def start_health_check(port=8080):
    server = HTTPServer(('', port), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
```

Добавьте в `price_monitor_service.py`:
```python
from health_check import start_health_check

# В main():
start_health_check(8080)
```

### 3. Уведомления о сбоях

Добавьте Telegram уведомления:

```bash
pip install python-telegram-bot
```

```python
# telegram_notifier.py
import requests

def send_telegram_message(message, token, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)
```

---

## 📥 Скачивание логов с облака

### Railway / Render
```bash
# Через CLI
railway run cat logs/market_2026-01-18.json > local_backup.json
```

### DigitalOcean / VPS
```bash
# SCP
scp -r root@ip:/opt/polymarket-logger/logs ./backup/

# RSYNC (более эффективно)
rsync -avz root@ip:/opt/polymarket-logger/logs/ ./backup/
```

### Fly.io
```bash
fly ssh console
# Затем в консоли сервера:
cat logs/market_2026-01-18.json
```

---

## 🎯 Мои рекомендации

### Для новичков:
**Railway** - самый простой, работает из коробки.

### Для бесплатного решения:
**Oracle Cloud Free Tier** - навсегда бесплатно, но требует времени на настройку.

### Для баланса цена/качество:
**DigitalOcean Droplet** - $4/месяц, полный контроль, надежно.

### Для разработчиков:
**Fly.io** - современный подход, отличный CLI, хороший free tier.

---

## 🔒 Безопасность

### Основные правила:

1. **Не храните секреты в коде**
   - Используйте переменные окружения
   - Добавьте `config.json` в `.gitignore`

2. **SSH ключи вместо паролей**
   ```bash
   ssh-keygen -t ed25519
   ssh-copy-id root@your_server_ip
   ```

3. **Firewall**
   ```bash
   # DigitalOcean
   ufw allow 22/tcp
   ufw enable
   ```

4. **Автоматические обновления**
   ```bash
   apt install unattended-upgrades
   dpkg-reconfigure --priority=low unattended-upgrades
   ```

---

## 📋 Чеклист развертывания

- [ ] Выбрана облачная платформа
- [ ] Создан аккаунт
- [ ] Проект загружен
- [ ] Установлены зависимости
- [ ] Настроен config.json
- [ ] Сервис запущен
- [ ] Проверены логи
- [ ] Настроен автозапуск
- [ ] Настроен мониторинг
- [ ] Настроен backup логов

---

## 💡 Pro Tips

1. **Регулярный backup**
   ```bash
   # Cron job для ежедневного backup
   0 2 * * * rsync -avz /opt/polymarket-logger/logs/ /backup/
   ```

2. **Ротация старых логов**
   ```bash
   # Удаление логов старше 30 дней
   find /opt/polymarket-logger/logs/ -name "*.json" -mtime +30 -delete
   ```

3. **Мониторинг дискового пространства**
   ```bash
   df -h
   ```

4. **Автоматический рестарт при сбое**
   - Railway/Render - автоматически
   - Systemd - `Restart=always`
   - Screen/tmux - используйте systemd

---

## 🚀 Быстрый старт (Railway)

```bash
# 1. Установка Railway CLI
npm install -g @railway/cli

# 2. Логин
railway login

# 3. Создание проекта
cd C:\Poly\Price_logger
railway init

# 4. Деплой
railway up

# 5. Просмотр логов
railway logs

# Готово! Сервис работает в облаке!
```

---

**Рекомендация:** Начните с **Railway** или **Oracle Cloud Free Tier**. Railway - если нужно быстро, Oracle - если хотите бесплатно навсегда.
