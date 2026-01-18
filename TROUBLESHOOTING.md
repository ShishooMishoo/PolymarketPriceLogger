# Troubleshooting - Polymarket Price Logger

Документ с описанием проблем, возникших при разработке, и их решений.

---

## Проблема 1: Ошибка API 422 при запросе деталей рынка

### Симптомы
```
Ошибка API: 422
Ошибка: не удалось получить данные для рынка 0xe90b27f08082e17740308fdc957528d29a3f334a9ecaeefd056a3427a4cfdaaf
```

### Причина
Gamma API не принимает `condition_id` в URL path формате (`/markets/{condition_id}`). API ожидает параметры через query string.

### Решение
Изменить метод запроса с:
```python
url = f"{GAMMA_API_BASE}/markets/{market_id}"
response = requests.get(url, timeout=10)
```

На:
```python
url = f"{GAMMA_API_BASE}/markets"
params = {"slug": market_id}
response = requests.get(url, params=params, timeout=10)
```

**Важно:** Использовать `slug` вместо `condition_id` для получения информации о рынке.

---

## Проблема 2: Неправильная фильтрация по condition_id

### Симптомы
При запросе с параметром `condition_id` API возвращает неправильные рынки (например, старые рынки 2020 года вместо Portugal Presidential Election 2026).

### Причина
Параметр `condition_id` в Gamma API работает некорректно и возвращает произвольные рынки вместо фильтрации по конкретному condition_id.

### Решение
Использовать параметр `slug` вместо `condition_id`:
```python
params = {"slug": "will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643"}
```

**Как найти slug:**
1. Откройте рынок на polymarket.com
2. URL: `https://polymarket.com/event/portugal-presidential-election/will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643`
3. Slug - это последняя часть URL после `/`

---

## Проблема 3: Ошибка API 400 при запросе цен

### Симптомы
```
Ошибка API цен: 400
Ошибка: не удалось получить цены для токена 28238304963115391468520084611709080022027216241044579007402765414035709535435
```

### Причина
CLOB API endpoint `/price` требует обязательный параметр `side` (buy или sell), но в коде этот параметр не передавался.

Ответ API при отсутствии параметра:
```json
{"error": "Invalid side"}
```

### Решение
Необходимо делать два отдельных запроса для получения bid и ask:

```python
# Получаем bid (цена покупки)
response_buy = requests.get(url, params={"token_id": token_id, "side": "buy"}, timeout=10)

# Получаем ask (цена продажи)
response_sell = requests.get(url, params={"token_id": token_id, "side": "sell"}, timeout=10)
```

Затем извлечь цены из ответов:
```python
bid = float(bid_data.get('price', 0)) if bid_data.get('price') else None
ask = float(ask_data.get('price', 0)) if ask_data.get('price') else None
mid = (bid + ask) / 2 if bid and ask else None
```

**Важно:**
- `side=buy` возвращает цену покупки (bid)
- `side=sell` возвращает цену продажи (ask)
- `mid` вычисляется как среднее между bid и ask

---

## Проблема 4: UnicodeEncodeError в Windows консоли

### Симптомы
```
UnicodeEncodeError: 'charmap' codec can't encode characters in position 0-6: character maps to <undefined>
```

Возникает при выводе русского текста или специальных символов (например, "João").

### Причина
По умолчанию Windows консоль использует кодировку cp1252, которая не поддерживает кириллицу и многие специальные символы.

### Решение
Перенастроить stdout на UTF-8 в начале функции:

```python
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

Это нужно делать перед любым выводом в консоль, содержащим не-ASCII символы.

---

## Проблема 5: Неправильная структура данных clobTokenIds

### Симптомы
Не удается извлечь token_id из ответа API.

### Причина
Поле `clobTokenIds` в ответе API может быть как строкой JSON, так и уже распарсенным массивом, в зависимости от версии API или типа запроса.

### Решение
Проверять тип данных и парсить при необходимости:

```python
clob_token_ids = market_details.get('clobTokenIds')
token_ids = json.loads(clob_token_ids) if isinstance(clob_token_ids, str) else clob_token_ids

# Берем первый токен (YES)
token_id = token_ids[0] if isinstance(token_ids, list) and len(token_ids) > 0 else None
```

**Важно:** Первый токен в массиве - это всегда токен "YES", второй - "NO".

---

## Проблема 6: Отсутствие токенов в старом API формате

### Симптомы
```
Ошибка: рынок не содержит токенов
```

### Причина
Старые рынки использовали поле `tokens` вместо `clobTokenIds`. Новые рынки используют только `clobTokenIds`.

### Решение
Использовать только `clobTokenIds` для всех современных рынков:

```python
clob_token_ids = market_details.get('clobTokenIds')
if not clob_token_ids:
    print("Ошибка: рынок не содержит токенов")
    return None
```

Не пытаться использовать поле `tokens` - это устаревший формат.

---

## Общие рекомендации

### API Endpoints
- **Gamma API:** `https://gamma-api.polymarket.com` - для получения информации о рынках
- **CLOB API:** `https://clob.polymarket.com` - для получения цен

### Структура запросов

1. **Получение информации о рынке:**
   ```
   GET https://gamma-api.polymarket.com/markets?slug={market_slug}
   ```

2. **Получение цены bid:**
   ```
   GET https://clob.polymarket.com/price?token_id={token_id}&side=buy
   ```

3. **Получение цены ask:**
   ```
   GET https://clob.polymarket.com/price?token_id={token_id}&side=sell
   ```

### Таймауты
Всегда устанавливать timeout для HTTP запросов (рекомендуется 10 секунд):
```python
response = requests.get(url, params=params, timeout=10)
```

### Обработка ошибок
Всегда проверять:
1. HTTP статус код (200 = успех)
2. Наличие данных в ответе
3. Корректность структуры данных

### Кодировка файлов
При работе с JSON файлами всегда указывать UTF-8:
```python
with open(log_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

Параметр `ensure_ascii=False` важен для корректного сохранения не-ASCII символов (кириллица, специальные символы).

---

## Полезные команды для отладки

### Тестирование API через curl

```bash
# Получить информацию о рынке
curl "https://gamma-api.polymarket.com/markets?slug=will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643"

# Получить bid цену
curl "https://clob.polymarket.com/price?token_id=28238304963115391468520084611709080022027216241044579007402765414035709535435&side=buy"

# Получить ask цену
curl "https://clob.polymarket.com/price?token_id=28238304963115391468520084611709080022027216241044579007402765414035709535435&side=sell"
```

### Тестирование отдельных функций

```python
from polymarket_price_logger import get_market_details, get_current_price

# Тест получения деталей рынка
market = get_market_details("will-joo-cotrim-figueiredo-win-the-2026-portugal-presidential-election-643")
print(market['question'])
print(market['clobTokenIds'])

# Тест получения цен
token_id = "28238304963115391468520084611709080022027216241044579007402765414035709535435"
prices = get_current_price(token_id)
print(prices)
```

---

## История изменений

**2026-01-18:** Документ создан на основе проблем, возникших при разработке Price Logger для Portugal Presidential Election.
