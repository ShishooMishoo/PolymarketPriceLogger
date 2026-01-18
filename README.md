# Polymarket Price Logger

Инструменты для мониторинга и логирования цен bid/ask на рынках Polymarket.

## Два режима работы

### 1. Простой скрипт (polymarket_price_logger.py)
Мониторинг одного рынка в течение заданного времени.

### 2. Сервис (price_monitor_service.py) ⭐ Рекомендуется
Непрерывный мониторинг нескольких рынков с горячей перезагрузкой конфигурации.

---

## Быстрый старт сервиса

### 1. Установка
```bash
pip install -r requirements.txt
```

### 2. Настройка
Отредактируйте `config.json`:
```json
{
  "markets": [
    {
      "slug": "your-market-slug",
      "name": "Market Name",
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

### 3. Запуск
**Windows:**
```bash
start_service.bat
```

**Linux/Mac:**
```bash
python price_monitor_service.py
```

📖 **Подробная документация:** [SERVICE_GUIDE.md](SERVICE_GUIDE.md)

---

## 📤 Загрузка на GitHub

Перед развертыванием в облаке загрузите проект на GitHub:

### Автоматический способ:
1. Создайте репозиторий на [github.com/new](https://github.com/new)
2. Запустите: **`upload_to_github.bat`**
3. Следуйте инструкциям в окне

### Ручной способ:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

📖 **Инструкции:**
- **Быстрая шпаргалка:** [GITHUB_QUICK.md](GITHUB_QUICK.md) - 5 команд
- **Подробное руководство:** [GITHUB_GUIDE.md](GITHUB_GUIDE.md) - все детали

---

## ☁️ Развертывание в облаке

После загрузки на GitHub можно развернуть в облаке за 5 минут!

### Быстрые варианты:

| Платформа | Цена | Время настройки | Ссылка |
|-----------|------|-----------------|--------|
| **Railway** | $5/мес | 5 минут | [railway.app](https://railway.app) |
| **Oracle Cloud** | **Бесплатно!** | 20 минут | [oracle.com/cloud/free](https://oracle.com/cloud/free) |
| **DigitalOcean** | $4/мес | 15 минут | [digitalocean.com](https://digitalocean.com) |

📖 **Инструкции по развертыванию:**
- **Быстрый старт:** [DEPLOY_QUICK.md](DEPLOY_QUICK.md) (3 простых варианта)
- **Полное руководство:** [CLOUD_DEPLOYMENT.md](CLOUD_DEPLOYMENT.md) (все платформы)

---

## Использование простого скрипта

## Установка

```bash
pip install -r requirements.txt
```

## Использование

### Базовое использование

```python
from polymarket_price_logger import log_market_prices

# Мониторинг рынка в течение 60 минут
log_market_prices(
    market_id="will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643",
    duration_minutes=60,
    log_file="prices.json"
)
```

### Параметры

- `market_id` (str): Slug рынка Polymarket
- `duration_minutes` (int, optional): Длительность мониторинга в минутах. `None` = бесконечно
- `log_file` (str): Имя JSON файла для сохранения данных

### Как найти market_id (slug)

1. Откройте рынок на polymarket.com
2. URL будет выглядеть так: `https://polymarket.com/event/portugal-presidential-election`
3. Нажмите на конкретный вопрос (например, "Will João Cotrim Figueiredo win?")
4. URL изменится на: `https://polymarket.com/event/portugal-presidential-election/will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`
5. Скопируйте последнюю часть после последнего `/` - это и есть slug: `will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`

### Формат данных

```json
[
  {
    "timestamp": "2026-01-18T12:30:00",
    "market_id": "0x1234...",
    "market_name": "Will Trump win 2024?",
    "token_id": "12345",
    "bid": 0.52,
    "ask": 0.54,
    "mid": 0.53
  }
]
```

## Примеры

### Мониторинг 1 час
```bash
python example.py
```

### Бесконечный мониторинг
Измените `duration_minutes=None` в example.py и остановите через Ctrl+C

## API Endpoints

- Gamma API: `https://gamma-api.polymarket.com`
- CLOB API: `https://clob.polymarket.com`
