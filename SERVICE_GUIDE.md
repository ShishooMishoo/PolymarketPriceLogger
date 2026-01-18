# Polymarket Price Monitor Service - Руководство

Сервис для непрерывного мониторинга множества рынков Polymarket с возможностью горячей перезагрузки конфигурации.

## Возможности

- ✅ Мониторинг нескольких рынков одновременно
- ✅ Каждый рынок записывается в отдельный файл
- ✅ Горячая перезагрузка конфигурации без остановки сервиса
- ✅ Автоматическое создание новых файлов каждый день
- ✅ Многопоточность - каждый рынок в своем потоке
- ✅ Обработка ошибок и переподключение

## Быстрый старт

### 1. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 2. Настройка конфигурации
Отредактируйте файл `config.json`:

```json
{
  "markets": [
    {
      "slug": "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643",
      "name": "Portugal Election - João Cotrim Figueiredo",
      "enabled": true
    }
  ],
  "settings": {
    "poll_interval_seconds": 60,
    "config_reload_interval_seconds": 30,
    "output_directory": "logs",
    "log_format": "{slug}_{date}.json"
  }
}
```

### 3. Запуск сервиса

**Windows:**
```bash
start_service.bat
```

**Linux/Mac:**
```bash
python price_monitor_service.py
```

### 4. Остановка
Нажмите `Ctrl+C`

## Конфигурация

### Структура config.json

#### Раздел `markets`
Массив рынков для мониторинга:

```json
{
  "slug": "market-slug-from-url",
  "name": "Отображаемое имя (опционально)",
  "enabled": true
}
```

- `slug` (обязательно) - идентификатор рынка из URL Polymarket
- `name` (опционально) - удобное имя для логов
- `enabled` (по умолчанию true) - включен ли мониторинг этого рынка

**Как найти slug:**
1. Откройте рынок на polymarket.com
2. Нажмите на конкретный вопрос
3. Скопируйте последнюю часть URL
4. Пример: `https://polymarket.com/event/portugal-presidential-election/will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`
5. Slug: `will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`

#### Раздел `settings`

```json
{
  "poll_interval_seconds": 60,
  "config_reload_interval_seconds": 30,
  "output_directory": "logs",
  "log_format": "{slug}_{date}.json"
}
```

- `poll_interval_seconds` - интервал между запросами цен (в секундах)
- `config_reload_interval_seconds` - как часто проверять изменения в config.json
- `output_directory` - директория для сохранения логов
- `log_format` - формат имени файла (не используется сейчас, зарезервировано)

## Горячая перезагрузка конфигурации

Сервис автоматически отслеживает изменения в `config.json` каждые 30 секунд (настраивается).

### Добавление нового рынка

1. Откройте `config.json`
2. Добавьте новый объект в массив `markets`:
```json
{
  "slug": "new-market-slug",
  "name": "New Market Name",
  "enabled": true
}
```
3. Сохраните файл
4. Через 30 секунд сервис автоматически запустит мониторинг нового рынка

### Отключение рынка

Измените `enabled` на `false`:
```json
{
  "slug": "market-to-disable",
  "name": "Market Name",
  "enabled": false
}
```

Или удалите рынок из массива `markets`.

### Изменение настроек

Изменения в секции `settings` требуют перезапуска сервиса.

## Структура выходных файлов

### Формат имени файла
```
{slug}_{date}.json
```

Пример:
```
will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643_2026-01-18.json
```

### Формат данных

```json
[
  {
    "timestamp": "2026-01-18T12:30:00.123456",
    "market_slug": "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643",
    "market_name": "Will João Cotrim Figueiredo win the 2026 Portugal presidential election?",
    "token_id": "28238304963115391468520084611709080022027216241044579007402765414035709535435",
    "bid": 0.162,
    "ask": 0.164,
    "mid": 0.163
  },
  {
    "timestamp": "2026-01-18T12:31:00.234567",
    "market_slug": "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643",
    "market_name": "Will João Cotrim Figueiredo win the 2026 Portugal presidential election?",
    "token_id": "28238304963115391468520084611709080022027216241044579007402765414035709535435",
    "bid": 0.161,
    "ask": 0.165,
    "mid": 0.163
  }
]
```

### Ротация файлов

Каждый день в 00:00 автоматически создается новый файл с текущей датой. Старые файлы сохраняются.

## Логи консоли

Пример вывода:
```
============================================================
Polymarket Price Monitor Service
============================================================

Запуск монитора: Portugal Election - João Cotrim Figueiredo
[Portugal Election - João Cotrim Figueiredo] Инициализация завершена
[Portugal Election - João Cotrim Figueiredo] Запуск мониторинга...

Запущено мониторов: 1
Директория для логов: logs
Интервал опроса: 60 секунд
Файл конфигурации: config.json

Для остановки нажмите Ctrl+C
============================================================

[Portugal Election - João Cotrim Figueiredo] [2026-01-18 12:30:00] Запись #1: Bid=0.162, Ask=0.164, Mid=0.163
[Portugal Election - João Cotrim Figueiredo] [2026-01-18 12:31:00] Запись #2: Bid=0.161, Ask=0.165, Mid=0.163
[Config Reloader] Обнаружены изменения в конфигурации
[Config Reloader] Запуск нового монитора: New Market Name
[Config Reloader] Конфигурация обновлена
```

## Примеры конфигураций

### Мониторинг одного рынка
```json
{
  "markets": [
    {
      "slug": "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643",
      "name": "Portugal Election",
      "enabled": true
    }
  ],
  "settings": {
    "poll_interval_seconds": 60,
    "config_reload_interval_seconds": 30,
    "output_directory": "logs"
  }
}
```

### Мониторинг нескольких рынков
```json
{
  "markets": [
    {
      "slug": "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643",
      "name": "Portugal - Cotrim Figueiredo",
      "enabled": true
    },
    {
      "slug": "will-andre-ventura-win-the-2026-portugal-presidential-election-643",
      "name": "Portugal - André Ventura",
      "enabled": true
    },
    {
      "slug": "will-marta-temido-win-the-2026-portugal-presidential-election-643",
      "name": "Portugal - Marta Temido",
      "enabled": false
    }
  ],
  "settings": {
    "poll_interval_seconds": 60,
    "config_reload_interval_seconds": 30,
    "output_directory": "portugal_election_logs"
  }
}
```

### Быстрое обновление (каждые 30 секунд)
```json
{
  "markets": [
    {
      "slug": "market-slug",
      "name": "High Frequency Market",
      "enabled": true
    }
  ],
  "settings": {
    "poll_interval_seconds": 30,
    "config_reload_interval_seconds": 10,
    "output_directory": "fast_logs"
  }
}
```

## Обработка ошибок

### Рынок не найден
```
[Market Name] Ошибка: не удалось получить детали рынка
```
**Решение:** Проверьте правильность slug в config.json

### Не удалось получить цены
```
[Market Name] Не удалось получить цены
```
**Решение:** Временная проблема с API. Сервис продолжит попытки автоматически.

### Ошибка записи в файл
```
[Market Name] Ошибка записи в файл: [детали]
```
**Решение:** Проверьте права доступа к директории логов.

## Производительность

- Каждый рынок работает в отдельном потоке
- Рекомендуется не более 10-20 рынков одновременно
- Минимальный интервал опроса: 10 секунд (для избежания rate limiting)

## API Rate Limits

Polymarket API может иметь ограничения на количество запросов:
- Рекомендуемый интервал: 60 секунд
- При мониторинге 10 рынков: 10 запросов в минуту
- Если получаете ошибки 429, увеличьте `poll_interval_seconds`

## Системные требования

- Python 3.7+
- 50 MB свободного места на диск (на 1 рынок, 1 месяц данных)
- Постоянное интернет-соединение
- Windows/Linux/MacOS

## Backup и восстановление

### Backup
Регулярно создавайте резервные копии:
```bash
# Windows
xcopy logs logs_backup\ /E /I /Y

# Linux/Mac
cp -r logs logs_backup
```

### Восстановление
Просто скопируйте файлы обратно в директорию `logs`.

## Запуск как службы (Windows)

Для автоматического запуска при загрузке системы используйте Task Scheduler:

1. Откройте Task Scheduler
2. Создайте новую задачу
3. Триггер: "При запуске системы"
4. Действие: Запустить `start_service.bat`
5. Настройте перезапуск при сбое

## Запуск как службы (Linux)

Создайте systemd service:

```ini
[Unit]
Description=Polymarket Price Monitor Service
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/Price_logger
ExecStart=/usr/bin/python3 price_monitor_service.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Сохраните как `/etc/systemd/system/polymarket-monitor.service` и запустите:
```bash
sudo systemctl enable polymarket-monitor
sudo systemctl start polymarket-monitor
```

## FAQ

**Q: Можно ли изменить интервал опроса без перезапуска?**
A: Нет, изменения в `settings` требуют перезапуска сервиса.

**Q: Что происходит с данными при перезапуске?**
A: Все данные сохраняются в файлах и не теряются при перезапуске.

**Q: Можно ли мониторить один рынок дважды с разными интервалами?**
A: Нет, каждый slug может быть в конфиге только один раз.

**Q: Как посмотреть статус работающего сервиса?**
A: Смотрите логи в консоли или проверяйте файлы в директории logs.

**Q: Занимает ли сервис много ресурсов?**
A: Нет, использование CPU и памяти минимально (< 50 MB RAM).

## Контакты и поддержка

При возникновении проблем проверьте:
1. `TROUBLESHOOTING.md` - решение частых проблем
2. Логи консоли - сообщения об ошибках
3. Файл конфигурации - правильность синтаксиса JSON
